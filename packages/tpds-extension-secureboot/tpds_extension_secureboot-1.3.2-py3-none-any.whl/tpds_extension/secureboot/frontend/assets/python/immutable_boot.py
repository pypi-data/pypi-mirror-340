import os
import cryptography
import tpds.tp_utils.tp_input_dialog as tp_userinput
from intelhex import IntelHex
from cryptography.hazmat.primitives import hashes
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.tp_utils.tp_utils import sign_on_host
from tpds.tp_utils.tp_utils import pretty_print_hex


class ImmutableBoot:
    def __init__(
        self,
        boards,
        app_start_addr=0x0000B000,
        app_end_addr=0x0003FAFF,
        sign_start_addr=0x0003FB00,
        publickey_start_addr=0x00009F00,
        app_len_str_addr=0x0003FD00,
    ):
        self.boards = boards
        self.app_start_addr = app_start_addr
        self.app_end_addr = app_end_addr
        self.sign_start_addr = sign_start_addr
        self.publickey_start_addr = publickey_start_addr
        self.app_len_str_addr = app_len_str_addr
        self.app_hex = None
        self.signature = None

    # Step1
    def generate_resources(self, b=None):
        # Generate Private Public Key pair
        print("Generating crypto assets for Usecase...", canvas=b)
        self.secbootkey = TPAsymmetricKey(self.__get_private_key_file(b))
        self.secbootkey.get_private_pem("private_key.pem")
        print(
            f"Public Key Bytes:\n{self.secbootkey.get_public_key_bytes().hex().upper()}"
        )
        print("Completed.")

    # Step2
    def boot_flash_with_publickey(self, b=None):
        # Add public key to boot hex image
        print("Generating BOOT hex...", end="", canvas=b)
        boot_hex = IntelHex()
        boot_hex.fromfile(self.__get_hex_file(b), format="hex")
        boot_hex.puts(self.publickey_start_addr, self.secbootkey.get_public_key_bytes())
        print("Completed.", canvas=b)
        # boot_hex.write_hex_file("boot_with_publickey.hex")

        # flash boot image
        print(f"Programming boot hex...", canvas=b)
        self.__flash_hex(boot_hex)
        print("Success", canvas=b)

    # Step3
    def sign_user_application_hex(self, b=None):
        print("Load APP hex File...", canvas=b)
        self.app_hex = IntelHex()
        self.app_hex.fromfile(self.__get_hex_file(b), format="hex")
        addrs = self.app_hex.segments()
        (unused, self.end_addr) = addrs[len(addrs) - 2]
        digest_data = self.app_hex.tobinarray(
            start=self.app_start_addr, size=(self.end_addr - self.app_start_addr)
        )
        # self.app_hex.write_hex_file("app_without_signature.hex")

        # calculate app digest
        print("\nHashing " + str(len(digest_data)) + " bytes in app Region")
        digest_obj = hashes.Hash(
            hashes.SHA256(), backend=cryptography.hazmat.backends.default_backend()
        )
        digest_obj.update(digest_data)
        app_digest = digest_obj.finalize()[:32]
        print(f"Digest: {pretty_print_hex(app_digest)}", canvas=b)

        # sign the app digest with private key (create app_signature)
        self.signature = sign_on_host(app_digest, self.secbootkey.get_private_key())
        print(f"Signature: {pretty_print_hex(self.signature)}", canvas=b)

    # step4
    def append_signature_to_app_hex(self, b=None):
        # Add signature to app hex image
        print("Adding signature to app_hex")
        self.app_hex.puts(self.sign_start_addr, self.signature)

        # Append application length
        app_len = self.end_addr - self.app_start_addr
        self.app_hex.puts(self.app_len_str_addr, app_len.to_bytes(4, "little"))
        # self.app_hex.write_hex_file("app_with_signature.hex")

    # Step5
    def app_flash_with_signature(self, b=None):
        print(f"Programming application hex...", canvas=b)
        self.__flash_hex(self.app_hex, addl_args=["-OP0-0000AFFF"])
        print("Success", canvas=b)

    def __get_private_key_file(self, b=None):
        print("Select secure boot private key option", canvas=b)
        item_list = ["Generate Private key", "Upload Private key"]
        dropdown_desc = """<font color=#0000ff><b>Select Secure Boot private key option</b>
        </font><br>
        <br>Generate Private key - Generates new Secure Boot private key<br>
        Upload Private key - Use existing private key file. Requires
        private key file .pem<br>"""
        user_input = tp_userinput.TPInputDropdown(
            item_list=item_list,
            desc=dropdown_desc,
            dialog_title="Private key selection",
        )
        user_input.invoke_dialog()
        print(f"Selected option is: {user_input.user_option}", canvas=b)
        assert user_input.user_option is not None, "Select valid private key Option"

        if user_input.user_option == "Upload Private key":
            print("Select private key file...", canvas=b)
            privkey = tp_userinput.TPInputFileUpload(
                file_filter=["*.pem"],
                nav_dir=os.getcwd(),
                dialog_title="Upload Private key",
            )
            privkey.invoke_dialog()
            print(f"Selected private key file is: {privkey.file_selection}", canvas=b)
            assert privkey.file_selection is not None, "Select valid private key file"
            return privkey.file_selection
        else:
            return None

    def __get_hex_file(self, b=None):
        print("Select hex file to load...", canvas=b)
        hexfile = tp_userinput.TPInputFileUpload(
            file_filter=["*.hex"], nav_dir=os.getcwd(), dialog_title="Upload Hex File"
        )
        hexfile.invoke_dialog()
        print(f"Selected hex file is: {hexfile.file_selection}", canvas=b)
        assert hexfile.file_selection is not None, "Select valid hex file"
        return hexfile.file_selection

    def __flash_hex(self, hex_obj, addl_args=[]):
        assert self.boards.get_selected_board(), "Select board to run an Usecase"
        temp_file = "ipe_load.hex"
        hex_obj.write_hex_file(temp_file)
        flash_firmware = FlashProgram(board_name="EV06X38A")
        assert flash_firmware.is_board_connected(), "Check the board connections"
        flash_firmware.load_hex_image_with_ipe(temp_file, addl_args=addl_args)
