Running the tool with empty files:

hsmsfmdgen.exe -s SecureFlashPageEmpty.xml -m RiversideFwMdEmpty.xml -d outputfwmd.hex -o outputsfp.hex
hsmsfmdgen.exe -s SecureFlashPageEmpty.xml -m UnicornFwMdOnlyHsm.xml -d unicornfwmdOnlyHsm.hex -o outputsfp.hex
hsmsfmdgen.exe -s SecureFlashPageEmpty.xml -m UnicornFwMdUnified.xml -d unicornfwmdUnified.hex -o outputsfp.hex


Just the Secure Flash File Empty with Verilog FPGA format
hsmsfmdgen.exe -s SecureFlashPageEmpty.xml -f  -o outputsfpemptyfpga.hex

Just the Secure Flash File Empty with Microchip Hex format
hsmsfmdgen.exe -s SecureFlashPageEmpty.xml  -o outputsfpempty.hex

Just the Secure Flash File With Keys with Verilog FPGA format
hsmsfmdgen.exe -s SecureFlashPage0.xml -f -o outputsfpfpga.hex

Just the Secure Flash File With Keys with Microchip Hex format
hsmsfmdgen.exe -s SecureFlashPage0.xml  -o outputsfp.hex

Quick Silver with dummy FPGA formated binary input files and XSD schema checking
hsmsfmdgen.exe -s SecureFlashPageQS.xml -m QuickSilverMd.xml -x hsmSecureFlash.xsd -y FirmwareMetadata.xsd -d outputfwmd.hex -o outputs.hex -f

The -l option is activate logging.  This is used for both crash detection and hang detection.  It accesses the drive a fair amount.  It is not recomended to use this on a network drive.
