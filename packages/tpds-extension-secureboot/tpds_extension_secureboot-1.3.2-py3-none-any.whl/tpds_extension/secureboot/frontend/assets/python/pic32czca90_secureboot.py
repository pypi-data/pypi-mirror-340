# select the mode in step 1 production or secure boot
# change the name of the HSM Custome flash page for production vs development
# save the key  and name the private key as specific to device and mode production vs development.
# Change the led app for production do it without hsm files.


import os
import shutil
import warnings
import time
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_print import print
from hsm_protocol import HSM
import os
from intelhex import IntelHex
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_print import print
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.helper import log
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils import run_subprocess_cmd
import hid
import xml.etree.ElementTree as ET
import tkinter as tk


warnings.filterwarnings('ignore')


class SecureBootUsecase:

    def __init__(self, boards, publickeylen=0, VID=0x04D8, PID=0x003F, secboot_publickey_slot=5, mode=None):
        self.boards = boards
        self.secboot_pulickey_slot = secboot_publickey_slot
        self.VID = VID
        self.PID = PID
        self.hsm_usb = hid.device()
        self.publickeylen = publickeylen
        self.mode = mode
        self.disable_sb = 0
        # Default values
        self.default_hsm_address = self.hsm_address = "0C7e0000"
        self.default_fwmd_address = self.fwmd_address = "0C7df800"
        self.default_start_address = self.start_address = "0C000000"
        self.default_app_size = self. app_size = "65536"

 # Step 1

    def generate_resources(self, b=None):
        self.__connect_to_SE(b)
        self.__get_dev_prod_mode(b)
        self.__secboot_pulickey_slotno(b)
        self.__gnerate_resources()
        print("\r\nSending Commands to HSM for Provisioning...")
        self.delete_slot(b)
        self.write_slot(b)
        self.write_nvm(b)
        self.read_slot(b)
        print("Completed.")

 # Step 2
    def app_hex(self, b=None):
        if (self.disable_sb == 1):
            print('Selected hex for disable secure boot...', canvas=b)
            self.app_image = os.path.join(
                os.getcwd(), 'pic32czca90_disable_secureboot.hex')
        else:
            print('Select Application image to create metadata...', canvas=b)
            hsm_flash = tp_userinput.TPInputFileUpload(
                file_filter=['*.hex'],
                nav_dir=os.getcwd(),
                dialog_title='Upload application hex file')
            hsm_flash.invoke_dialog()
            print(
                f'Selected file is: {hsm_flash.file_selection}',
                canvas=b)
            assert hsm_flash.file_selection is not None, \
                'Select valid application image file'
            self.app_image = hsm_flash.file_selection
        print(self.app_image)

        print('Select HSM image to create metadata...', canvas=b)
        hsm_flash = tp_userinput.TPInputFileUpload(
            file_filter=['*.hex'],
            nav_dir=os.getcwd(),
            dialog_title='Upload HSM hex file')
        hsm_flash.invoke_dialog()
        print(
            f'Selected file is: {hsm_flash.file_selection}',
            canvas=b)
        assert hsm_flash.file_selection is not None, \
            'Select valid HSM image file'
        self.HSM_image = hsm_flash.file_selection
        print(self.HSM_image)

 # Step 2a
    def prvkey_prod(self, b=None):
        print('Select private key file used for Secure Boot...', canvas=b)
        self.hsm_prvkeyfile = tp_userinput.TPInputFileUpload(
            file_filter=['*.pem'],
            nav_dir=os.getcwd(),
            dialog_title='Upload private key file')
        self.hsm_prvkeyfile.invoke_dialog()
        print(
            f'Selected file is: {self.hsm_prvkeyfile.file_selection}',
            canvas=b)
        assert self.hsm_prvkeyfile.file_selection is not None, \
            'Select valid private key file'
        self.secbootkey = TPAsymmetricKey(self.hsm_prvkeyfile.file_selection)
        # privkey_file = 'private_key_2a.pem'
        # self.secbootkey.get_private_pem(privkey_file)
        self.privatekey = self.secbootkey.get_private_key_bytes().hex().upper()
        # self.secbootkey.get_public_pem("public_key_2a.pem")
        self.publickey = self.secbootkey.get_public_key_bytes().hex().upper()
        # print(f"Private Key Bytes:", self.privatekey, canvas=b)
        # self.publickeylen = int(len(self.publickey)/2)
        # print(f"Public Key Bytes:", self.publickey, canvas=b)
        # 64 byte key


# Step 3

    def FWMDTool(self, b=None):
        self.FWMDT_input(b)
        self.FWMDT_xml_modify(b)
        self.run_FWMDtool(b)
# step 4

    def combined_hex(self, b=None):
        self.combined_hex_to_flash(b)
# Step 5

    def prog_FWMD(self, b=None):
        kit_parser = FlashProgram('EV16W43A')
        kit_parser.load_hex_image_with_ipe(self.combined_hex)
# Step 4a

    def disable_secureboot(self, b=None):
        self.disable_sb = 1
        self.prvkey_prod(b)
        self.app_hex(b)
        self.hsm_address = self.default_hsm_address
        self.fwmd_address = self.default_fwmd_address
        self.start_address = self.default_start_address
        self.app_size = self.default_app_size
        self.FWMDT_xml_modify(b)
        self.run_FWMDtool(b)
        self.combined_hex_to_flash(b)
        print(f"Execute step 5 to flash combined image to Disable Secure Boot")
        self.disable_sb = 0


#####################################################################################################################################################

    def __connect_to_SE(self, b=None):
        print('Connect to Secure Element: ', canvas=b)
        if self.boards is None:
            print('Prototyping board MUST be selected!', canvas=b)
            return
        assert self.boards.get_selected_board(), \
            'Select board to run an Usecase'

        self.device = 'EV16W43A'
        print(self.boards.get_selected_board().get("name"))
        self.kit_parser = FlashProgram('EV16W43A')
        print(self.kit_parser.check_board_status())
        assert self.kit_parser.is_board_connected(), \
            'Check the Kit parser board connections'
        factory_hex = self.boards.get_kit_hex()
        if not self.kit_parser.is_factory_programmed():
            assert factory_hex, \
                'Factory hex is unavailable to program'
            print('Programming factory hex...', canvas=b)
            tp_settings = TPSettings()
            path = os.path.join(
                tp_settings.get_tpds_core_path(),
                'assets', 'Factory_Program.X',
                factory_hex)
            print(f'Programming {path} file')
            self.kit_parser.load_hex_image_with_ipe(path)
            text_box_desc = (
                '''<font color=#0000ff><b>Reset the Board and press OK </b></font><br>
                    <br>To discover HSM and provision the keys<br>''')
            user_input = tp_userinput.TPMessageBox(
                info=text_box_desc,
                title='HSM',
                option_list='OK')
            user_input.invoke_dialog()

        assert self._discover_hsm() == HSM.hsm_found, \
            '\r\n   HSM not present:'\
            '\r\n   1. Reset the board'\
            '\r\n           OR'\
            '\r\n   2 . Power cycle the device'
        print("HSM Device found")

    def __gnerate_resources(self, b=None):

        self.publickeylen = 0
        print('\r\nGenerating crypto assets for Usecase...', canvas=b)
        self.secbootkey = TPAsymmetricKey(self.__get_private_key_file(b))
        privkey_file = 'private_key_'+self.mode+'.pem'
        self.secbootkey.get_private_pem(privkey_file)
        self.privatekey = self.secbootkey.get_private_key_bytes().hex().upper()
        self.secbootkey.get_public_pem('public_key_'+self.mode+'.pem')
        self.publickey = self.secbootkey.get_public_key_bytes().hex().upper()
        print(f"Private Key Bytes:", self.privatekey, canvas=b)
        self.publickeylen = int(len(self.publickey)/2)
        print(f"Public Key Bytes:", self.publickey, canvas=b)
        # 64 byte key

    def __secboot_pulickey_slotno(self, b=None):
        print(f'Selected HSM slot is: 5', canvas=b)
        self.secboot_pulickey_slot = 5
        HSM.hsm_slotinfo[0] = self.publickeylen + \
            HSM.HEADER_BYTES
        HSM.hsm_slotinfo[1] = self.secboot_pulickey_slot << 8
        HSM.hsm_slotinfo[4] = self.publickeylen

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
            print(
                f"Selected private key file is: {privkey.file_selection}", canvas=b)
            assert privkey.file_selection is not None, "Select valid private key file"
            return privkey.file_selection
        else:
            return None

    def __get_dev_prod_mode(self, b=None):

        print("Select Development mode or Production Mode", canvas=b)
        item_list = ["Development Mode", "Production Mode"]
        dropdown_desc = """<font color=#0000ff><b>Select Development or Production Mode Option</b>
        </font><br>
        <br>Development Mode- Executes Test Secure Boot mode that will not lock the device in case of authentication failure.<br>
                              The board can be re-programmed.<br>
                              <br>
            Production Mode - Executes Secure Boot mode and will lock the device in case of authentication failure.<br>
                              Can only be re-programmed by creating metadata with right private key pair.<br>"""
        user_input = tp_userinput.TPInputDropdown(
            item_list=item_list,
            desc=dropdown_desc,
            dialog_title="Development/Production Mode",
        )
        user_input.invoke_dialog()
        print(f"Selected option is: {user_input.user_option}", canvas=b)
        assert user_input.user_option is not None, "Select valid Option"

        if user_input.user_option == "Development Mode":
            self.mode = 'dev'
            self.sbc = 0
            self.changesbc(b)
            self.write_nvm(b)
            self.test_sbc = 2
            self.changetestsbc(b)  # test mode for sequential secure boot
            self.write_nvm(b)
            print("Sent commands for development mode")
        if user_input.user_option == "Production Mode":
            self.mode = 'prod'
            self.test_sbc = 0
            self.changetestsbc(b)  # test mode for sequential secure boot
            self.write_nvm(b)
            self.sbc = 2
            self.changesbc(b)
            self.write_nvm(b)
            (f"Sent commands for production mode")

    def delete_slot(self, b=None):
        self._delete_slot(self.secboot_pulickey_slot)

    def _delete_slot(self, slotnum, b=None):
        OUTDATA = b"\rhsm:talk(group[03]cmd[04]slot[%02x])\n" % slotnum
        self.__write_hsm_hid(OUTDATA)

    def write_slot(self, b=None):
        assert self.publickeylen > 0, \
            "Generate Public Key Before Loading key to Slot"
        assert self._hsm_load_public_key(
            self.secboot_pulickey_slot,
            self.publickey,
            self.publickeylen) == "KIT_STATUS_SUCCESS", \
            "HSM Key Load Failed"
        print("     HSM Write Complete", canvas=b)

    def _hsm_load_public_key(self, slot, key, keylen, b=None):
        hsm_wr_cmd = self.__combine_cmd_dataforwrite(slot, key, keylen)
        cmdLength = len(hsm_wr_cmd)
        numFullHidBufs = int(cmdLength/(HSM.HIDBUFSIZEBYTES+1))
        for i in range(numFullHidBufs):
            cmd_datastr = hsm_wr_cmd[i*(HSM.HIDBUFSIZEBYTES-1)
                                        :((i+1)*(HSM.HIDBUFSIZEBYTES-1))]
            cmd_datastr = b"\r" + cmd_datastr
            self.__write_hsm_hid(cmd_datastr)
        remBufferBytes = cmdLength % (HSM.HIDBUFSIZEBYTES+1)
        if (remBufferBytes > 0):
            cmd_datastr = b"\r" + \
                hsm_wr_cmd[numFullHidBufs*(HSM.HIDBUFSIZEBYTES-1):]
            self.__write_hsm_hid(cmd_datastr)
            status = self.__hsm_read_resp()
        return (status)

    def __combine_cmd_dataforwrite(self, slot, key, keylen, b=None):

        dataLenWords = int((keylen/4) + (HSM.HEADER_BYTES)/4)
        OUTSTR = "hsm:talk(group[03]cmd[00]slot[%02x]length[%02x]" % (
            slot, (dataLenWords+1))
        print(" Sending Write Command...")
        OUTDATA = bytes(OUTSTR, 'utf-8')
        OUTKEY = bytes(key, 'utf-8')
        OUTDATA += b'data['
        for w in HSM.hsm_slotinfo:
            wle = int.from_bytes(w.to_bytes(4, byteorder='little'),
                                 byteorder='big',  signed=False)
            OUTDATA += bytes("%08x" % wle, 'utf-8')
        OUTDATA += OUTKEY
        OUTDATA += b"])\n"
        return (OUTDATA)

    def write_nvm(self, b=None):
        assert self._misc_write_nvm(self.secboot_pulickey_slot) == "KIT_STATUS_SUCCESS", \
            "       HSM NVM Write Failed"

    def _misc_write_nvm(self, b=None):
        OUTDATA = b"\rhsm:talk(group[F0]cmd[06])\n"
        self.__write_hsm_hid(OUTDATA)
        status = self.__hsm_read_resp()
        return (status)

    def changesbc(self, b=None):
        assert self._misc_write_sbc(self.secboot_pulickey_slot) == "KIT_STATUS_SUCCESS", \
            "       HSM SBC Failed"

    def _misc_write_sbc(self, b=None):
        print(" Sending secure boot configuration command ")
        # sb[2- sequential; 0- disable; 1 simultaneous];
        OUTDATA = b"\rhsm:talk(group[F0]cmd[04]sb[%02x])\n" % self.sbc
        self.__write_hsm_hid(OUTDATA)
        status = self.__hsm_read_resp()
        return (status)

    def changetestsbc(self, b=None):
        assert self._misc_write_test_sbc(self.secboot_pulickey_slot) == "KIT_STATUS_SUCCESS", \
            "       HSM SBC Failed"

    def _misc_write_test_sbc(self, b=None):
        print(" Sending Test secure boot configuration command ")
        # sb[2- sequential; 0- disable; 1 simultaneous];
        OUTDATA = b"\rhsm:talk(group[F0]cmd[0A]sb[%02x])\n" % self.test_sbc
        self.__write_hsm_hid(OUTDATA)
        status = self.__hsm_read_resp()
        return (status)

    def read_slot(self, b=None):
        assert self._hsm_read(self.secboot_pulickey_slot, self.publickeylen, info=None) == "KIT_STATUS_SUCCESS", \
            "HSM Read Failed, No Key in Slot"
        assert (self.key_length != b'00000000'), \
            'Provisionig is not successful, Restart from step 1'
        print("     Read Completed")

    def _hsm_read(self, slot, keylen, info, b=None):
        maxLength = int((keylen/8) + (HSM.HEADER_BYTES)/4)
        maxNumBuffs = HSM.MAXRSPLENGTH/HSM.HIDBUFSIZEBYTES
        print(" Sending Read Command...")
        if info == True:
            hsm_readcmd = self.__hsm_read_slotinf_cmd(slot, maxLength)
        else:
            hsm_readcmd = self.__hsm_read_slot_cmd(slot, maxLength)

        hsm_readcmdbtyes = bytes(hsm_readcmd, 'utf-8')
        self.__write_hsm_hid(hsm_readcmdbtyes)
        eoc = False
        rsp = b""
        rspLen = 0
        numBuffs = 0
        while (True):
            d = self.__read_hsm_hid(64)
            numBuffs += 1
            if d:
                ds = bytes(d)
                # print("\n %s" % (bytearray(d).hex('/', 1)))
                delIdx = ds.find(0x0a)
                if (delIdx > -1):
                    rspLen += delIdx
                    rsp += ds[:delIdx+1]
                    eoc = True
                    break
                else:
                    rsp += ds
                    rspLen += HSM.HIDBUFSIZEBYTES
            else:
                eoc = True
                break
            if (numBuffs > maxNumBuffs):
                break

        # print("RSP:  %s" % (rsp))
        self.kc = int(rsp[:2], 16)
        rc = int(rsp[3:11], 16)
        dStart = rsp.find(0x28)+1  # '('
        dEnd = rsp.find(0x29)  # ')'
        if (dEnd > 0):
            dLength = dEnd-dStart
            # print("Data length:  %d" % (dLength))
            dData = rsp[dStart:(dEnd)]
            dWords = int(dLength/(HSM.CHARSPERWORD))
            dRem = dLength % (HSM.CHARSPERWORD)
            # print(" Read Slot Info:")
            for i in range(dWords):
                ws = dStart + i*HSM.CHARSPERWORD
                # read_key = (rsp[ws:we])
                if (i <= 5):
                    we = ws + HSM.CHARSPERWORD
                    # print("  W%02d: %s " %
                    # (i, (rsp[ws:we])), HSM.slot_info_words[i])
                    if (i == 5):
                        self.key_length = (rsp[ws:we])

                else:
                    print(" Key in Slot %d:" % self.secboot_pulickey_slot)
                    print("   %s" % (rsp[ws:dEnd]))
                    self.slotkeybytes = (rsp[ws:dEnd])
                    break

            if (dRem > 0):
                print("  W%02d: %s" % (i, (rsp[we-dRem:we])))
            return (HSM.kcDictR[self.kc])

        else:
            print("VSM_SLOT_INFO Response Error!!!")

    def __hsm_read_slot_cmd(self, slotnum, dataLength, b=None):
        OUTSTR = "\rhsm:talk(group[03]cmd[01]slot[%02x]length[%02x])\n" % (
            slotnum, dataLength)
        # print(OUTSTR)
        return (OUTSTR)

    def __hsm_read_slotinf_cmd(self, slotnum, b=None):
        OUTSTR = "\rhsm:talk(group[03]cmd[05]slot[%02x])\n" % slotnum
        # print(OUTSTR)
        return (OUTSTR)

    def _discover_hsm(self, b=None):
        hsmdiscovercmd = b"\rboard:device(00)\n"
        self.__write_hsm_hid(hsmdiscovercmd)
        hsm_response = self.__read_hsm_hid(64)
        hsm_discover = bytes(hsm_response)
        hsm_response_str = hsm_discover.decode()
        return (hsm_response_str.find('HSM'))

    def __hsm_read_resp(self, b=None):
        d = ""
        d = self.__read_hsm_hid(64)
        if d:
            ds = bytes(d)
        kc = int(ds[:2], 16)
        return (HSM.kcDictR[kc])

    def __open_hid(self, b=None):
        self.hsm_usb = hid.device()
        self.hsm_usb.open(self.VID, self.PID)

    def __write_hsm_hid(self, msg, b=None):
        self.__open_hid()
        assert self.hsm_usb.write(msg), 'Not able to wirte the HSM'
        time.sleep(0.05)

    def __read_hsm_hid(self, byt, b=None):
        response = self.hsm_usb.read(byt)
        return response

    def combined_hex_to_flash(self, b=None):
        print('Combining Firmware metadata,HSM firmware and application image...', canvas=b)
        self.__create_combined_firmware(
            'FWmetadatatool\outputfwmd.hex', self.app_image)
        print("Created FWMD and combined image of FWMD,HSM firmware and application image")

    def __create_combined_firmware(self, img1, img2, b=None):
        if (self.disable_sb == 1):
            self.combined_hex = 'combined_sb_disable.hex'
        else:
            self.combined_hex = 'combined_sb.hex'

        self.combined = IntelHex()
        fwmd_hex = 'fwmd.hex'
        print("\r\n")
        fwmd_img_hex = os.path.join(os.getcwd(), img1)
        print(fwmd_img_hex)
        shutil.copy(fwmd_img_hex, fwmd_hex)
        self.combined.merge(IntelHex(fwmd_hex), overlap='replace')
        os.remove(fwmd_hex)
        app_hex = 'applicaion.hex'
        app_img_hex = os.path.join(os.getcwd(), img2)
        print("\r\n")
        print(app_img_hex)
        shutil.copy(app_img_hex, app_hex)
        self.combined.merge(IntelHex(app_hex), overlap='replace')
        os.remove(app_hex)
        self.combined.tofile(self.combined_hex, format='hex')
        print('Completed', canvas=b)
        print(f'Combined image file is: {self.combined_hex}', canvas=b)

    def FWMDT_input(self, b=None):
        def on_ok():
            self.hsm_address = hsm_entry.get()
            self.fwmd_address = fwmd_entry.get()
            self.start_address = start_entry.get()
            self.app_size = size_entry.get()
            root.destroy()

        def on_cancel():
            root.destroy()

        # Initialize the Tkinter root window
        root = tk.Tk()
        root.title("FWMD Tool")
        root.geometry("400x200")
        # Calculate the center position
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}")
        # Make the window appear in front of the parent
        root.transient(None)  # Tie it to the parent window
        root.lift()  # Raise it above all other windows
        root.attributes('-topmost', True)  # Keep it on top
        root.focus_set()  # Grab focus
        root.grab_set()  # Block interaction with the parent until closed

        # Labels and Entry widgets
        tk.Label(root, text="FWMD Address:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e")
        fwmd_entry = tk.Entry(root, width=30)
        fwmd_entry.grid(row=0, column=1, padx=10, pady=5)
        fwmd_entry.insert(0, self.default_fwmd_address)

        tk.Label(root, text="HSM Firmware Address(~2kbytes from FWMD):").grid(
            row=1, column=0, padx=10, pady=5, sticky="e")
        hsm_entry = tk.Entry(root, width=30)
        hsm_entry.grid(row=1, column=1, padx=10, pady=5)
        hsm_entry.insert(0, self.default_hsm_address)

        tk.Label(root, text=" App Start Address:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e")
        start_entry = tk.Entry(root, width=30)
        start_entry.grid(row=2, column=1, padx=10, pady=5)
        start_entry.insert(0, self.default_start_address)

        tk.Label(root, text="Validation Bytes from Start Address").grid(
            row=3, column=0, padx=10, pady=5, sticky="e")
        size_entry = tk.Entry(root, width=30)
        size_entry.grid(row=3, column=1, padx=10, pady=5)
        size_entry.insert(0, self.default_app_size)

        # OK and Cancel buttons
        ok_button = tk.Button(root, text="OK", command=on_ok)
        ok_button.grid(row=4, column=0, padx=10, pady=10)

        cancel_button = tk.Button(root, text="Cancel", command=on_cancel)
        cancel_button.grid(row=4, column=1, padx=10, pady=10)

        # Run the Tkinter event loop
        root.mainloop()
        # Print the values if OK was pressed
        try:
            print(f"HSM Firmware Address: {self.hsm_address}")
            print(f"FWMD Address: {self.fwmd_address}")
            print(f"Start Address of the Application: {self.start_address}")
            print(f"Size of the Application: {self.app_size}")
        except NameError:
            print("Operation was cancelled.")

    def FWMDT_xml_modify(self, b=None):

        # Load and parse the XML file,pic32czca90FwMd.xml

        self.path = os.path.join(os.getcwd(), 'FWmetadatatool')
        self.Metadatafile = 'pic32czca90FwMd.xml'
        self.fwmd1 = os.path.join(self.path,  self.Metadatafile)
        tree = ET.parse(self.fwmd1)
        root = tree.getroot()
        ET.register_namespace(
            "tns", "http://www.example.org/FirmwareMetadata")
        ET.register_namespace(
            "xsi", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace(
            "schemaLocation", "http://www.example.org/hsmSecureFlash hsmSecureFlash.xsd ")
        namespaces = {'tns': 'http://www.example.org/FirmwareMetadata',
                      'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                      'schemaLocation': 'http://www.example.org/hsmSecureFlash.xsd'}

# Update HSM Firmware srcAddress
        for image in root.findall('tns:image', namespaces):
            image_meta_data = image.find('tns:imageMetaData', namespaces)
            if image_meta_data is not None:
                image_type = image_meta_data.find('tns:type', namespaces)
                if image_type is not None and image_type.text == 'HSM Firmware':
                    src_address = image.find('tns:srcAddress', namespaces)
                    if src_address is not None:
                        src_address.text = self.hsm_address
                    HSM_hex = image.find('tns:imageFileInputPath', namespaces)
                    if HSM_hex is not None:
                        HSM_hex.text = self.HSM_image

# Update addressOfMetadata1
        address_of_metadata1 = root.find('tns:addressOfMetadata1', namespaces)
        if address_of_metadata1 is not None:
            address_of_metadata1.text = self.fwmd_address

# Update HOST Program Image srcAddress and maxSizeOfImage
        for image in root.findall('tns:image', namespaces):
            image_meta_data = image.find('tns:imageMetaData', namespaces)
            if image_meta_data is not None:
                image_type = image_meta_data.find('tns:type', namespaces)
            if image_type is not None and image_type.text == 'HOST Program Image':
                src_address = image.find('tns:srcAddress', namespaces)
                if src_address is not None:
                    src_address.text = self.start_address
                max_size_of_image = image.find(
                    'tns:maxSizeOfImage', namespaces)
                if max_size_of_image is not None:
                    max_size_of_image.text = self.app_size
                file_path = image.find('tns:imageFileInputPath', namespaces)
                if file_path is not None:
                    file_path.text = self.app_image
    # Save the modified XML back to the file
        tree.write(self.fwmd1, encoding='UTF-8', xml_declaration=True)
        # Replace with the actual path to your XML file
        print(f"Updated XML file saved to {self.fwmd1}")

    # update SourceFlash xml
        ET.register_namespace(
            "hsmsf", "http://www.example.org/hsmSecureFlash")
        ET.register_namespace(
            "xsi", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace(
            "schemaLocation", "http://www.example.org/hsmSecureFlash hsmSecureFlash.xsd ")
        namespace = {'hsmsf': 'http://www.example.org/hsmSecureFlash',
                     'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                     'schemaLocation': 'http://www.example.org/hsmSecureFlash.xsd'}
        self.sourceflash = os.path.join(self.path, 'SecureFlashPage0.xml')
        tree = ET.parse(self.sourceflash)
        root = tree.getroot()
        key_tag = root.find('.//hsmsf:privateKey/hsmsf:key', namespace)
        if key_tag is not None:
            key_tag.text = self.privatekey
        #
        tree.write(self.sourceflash, encoding='UTF-8', xml_declaration=True)
        print(f"Updated XML file saved to {self.sourceflash}")

    def run_FWMDtool(self, b=None):
        print("Creating Metadata...")
        self.tool = os.path.join(
            os.getcwd(), 'FWmetadatatool')
        self.tool_path = [str(self.tool)]
        self.FWMD_tool = os.path.join(self.tool, 'hsmsfmdgen.exe')
        FWMD_tool_path = [str(self.FWMD_tool)]
        FWMD_cmd = (
            FWMD_tool_path
            + [
                "-s",
                os.path.join(self.tool, "SecureFlashPage0.xml"),
                "-m",
                os.path.join(self.tool, "pic32czca90FwMd.xml"),
                "-x",
                os.path.join(self.tool, "hsmSecureFlash.xsd"),
                "-y",
                os.path.join(self.tool, "FirmwareMetadata.xsd"),
                "-d",
                os.path.join(self.tool, "outputfwmd.hex"),
                "-o",
                os.path.join(self.tool, "outputs.hex"),
            ]

        )
        print(FWMD_cmd)
        subprocessout = run_subprocess_cmd(cmd=FWMD_cmd)
        if not subprocessout:
            print("Error creating Metadata. Reset and start from Step 1")
        print(subprocessout)
        print("OK")
