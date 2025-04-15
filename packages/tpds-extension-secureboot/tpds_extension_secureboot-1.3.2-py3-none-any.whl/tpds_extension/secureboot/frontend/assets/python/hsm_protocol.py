class HSM():
    BYTESPERWORD = 4
    BITSPERWORD, prvkey_size = 32, 32
    HIDBUFSIZEBYTES = 64
    WORDSPERHIDBUFF = HIDBUFSIZEBYTES/BYTESPERWORD
    MAXRSPLENGTH = 2048
    CHARSPERWORD = BYTESPERWORD*2
    hsm_found = 0
    hsm_status_success = 0
    HEADER_BYTES = 16

    VSM_INPUT_RAW_DATA_WORDS = 8
    VSM_INPUT_RAW_METADATA_WORDS = 4
    VSM_INPUT_RAW_DATA_BITS = 8*BITSPERWORD
    VSM_INPUT_RAW_BYTES = VSM_INPUT_RAW_DATA_WORDS*BYTESPERWORD
    VSM_INPUT_RAW_BUFFERS = VSM_INPUT_RAW_BYTES/HIDBUFSIZEBYTES

    kcDict = {"KIT_STATUS_SUCCESS": 0x00,
              "KIT_STATUS_FAILURE": 0x01,
              "KIT_STATUS_COMMAND_NOT_VALID": 0x03,
              "KIT_STATUS_COMMAND_NOT_SUPPORTEDr": 0x04,
              "KIT_STATUS_NO_DEVICE": 0xC5,
              "KIT_STATUS_INVALID_PARAM": 0xE2,
              "KIT_STATUS_INVALID_ID": 0xE3,
              "KIT_STATUS_INVALID_SIZE": 0xE4,
              "KIT_STATUS_RX_FAIL": 0xE6,
              "KIT_STATUS_RX_NO_RESPONSE": 0xE7,
              "KIT_STATUS_TX_TIMEOUT": 0xEA,
              "KIT_STATUS_RX_TIMEOUT": 0xEB,
              "KIT_STATUS_SMALL_BUFFER": 0xED,
              "KIT_STATUS_COMM_FAIL": 0xF0,
              "KIT_STATUS_EXECUTION_ERROR": 0xF4,
              "KIT_STATUS_TX_FAIL": 0xF7}

    rcDict = {
        0x00000000: "E_UNKNOWN Unspecified failure",
        0x00000001: "S_OK Command was successful",
        0x80000000: "E_GENERAL General Unspecified Failure",
        0x80000001: "E_CMDCANCEL Command was Canceled",
        0x80000002: "E_NOTSUPPORTED Command not supported ",
        0x80000003: "E_INVPARAM Invalid Parameter",
        0x80000004: "E_INVINPUT Invalid Input",
        0x80000005: "E_INPUTDMA DMA Input Error",
        0x80000006: "E_OUTPUTDMA DMA Output Error",
        0x80000007: "E_SYSTEMMEM Error Accessing System Memory",
        0x80000008: "E_INPUTAUTH Error authenticating Input",
        0x80000009: "E_HSMFWAUTH Error authenticating HSM Firmware",
        0x8000000A: "E_HOSTFWAUTH Error Authenticating HOST firmware",
        0x8000000B: "E_SAFEMODE A critical error has occurred",
        0x8000000C: "E_SELFTEST ",
        0x8000000D: "E_TIMELOCKED",
        0x8000000E: "E_TIMEUNLOCKED time is currently unlocked",
        0x8000000F: "E_TMPRLOCKED requires the tamper response module",
        0x80000010: "E_TMPRUNLOCKED the tamper response",
        0x80000011: "E_VSINUSE Variable Slot is in used",
        0x80000012: "E_VSEMPTY Variable Slot is empty",
        0x80000013: "E_NOHSMFW No HSM FW was provided",
        0x80000014: "E_INVVS Invalid Variable slot. ",
        0x80000015: "E_HASHFAILED Secure Flash Page Hash Error",
        0x80000016: "E_FWMDAUTH Firmware Metadata Authentication Failed",
        0x80000017: "E_UNKNOWNSBC The flash pages have not been read yet",
        0x80000018: "E_CRYPTOHW There was an error",
        0x80000019: "E_OUTPUTNOTSET The output DMA descriptor",
        0x8000001A: "E_INPUTNOTSET The input DMA descriptor",
        0x8000001B: "E_OUTPUTSET The output DMA descriptor",
        0x8000001C: "E_INPUTSET The input DMA descriptor",
        0x8000001D: "E_AUTHBITSET The authentication set",
        0x8000001E: "E_AUTHBITNOTSET The authentication fields not set",
        0x8000001F: "E_SLOTPARASET",
        0x80000020: "E_SLOTPARANOTSET",
        0x80000021: "E_INVFORMAT ",
        0x80000022: "E_OUTPUTTOOSMALL",
        0x80000023: "E_OUTOFMEMORY",
        0x80000024: "E_INVHASHTYPE The hash type is invalid",
        0x80000025: "E_HOSTFLASHLCK Only valid during secure boot",
        0x80000026: "E_HOSTFLASHERASE An operation to erase failed",
        0x80000027: "E_HOSTFLASHREAD An operation to read failed",
        0x80000028: "E_HOSTFLASHWRITE An operation to write failed",
        0x80000029: "E_HSMFLASHLCK An operation to lock failed",
        0x8000002A: "E_HSMFLASHERASE An operation to erase failed",
        0x8000002B: "E_HSMFLASHREAD An operation to read failed",
        0x8000002C: "E_HSMFLASHWRITE An operation to write failed"}

    kcDictR = dict((value, key) for key, value in kcDict.items())

    hsm_slotinfo = [
        0x00000050,  # Data Length (76 bytes, 13 Words)
        0x00000F00,  # RAW Header Start with Slot number
        0x00000000,  # Not Valid Before
        0xFFFFFFFF,  # Not Valid After
        0x00000040,  # RAW Metadata:  just the length(64 bytes)
    ]
    slot_info_words = ['Read Status', 'Data Length', 'Slot Number',
                       '', '', 'Key Length ']
