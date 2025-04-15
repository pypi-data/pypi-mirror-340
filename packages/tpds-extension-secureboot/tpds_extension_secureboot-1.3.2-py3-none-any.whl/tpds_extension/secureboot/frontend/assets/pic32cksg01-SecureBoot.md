# Trust Platform Design Suite

Usecase Help –  Secure Boot - PIC32CKSG01
-----
This document helps to understand Pre and Post steps of Usecase transaction diagram.

Setup requirements
----

*	PIC32CK SG Curiosity Ultra Development Board
*	MPLAB X IDE v6.15 or above
# Pre Usecase transaction Steps
PIC32CKCG01

*	Connect PIC32CK SG01 Curiosity board to PC running Trust Platform Design Suite. Power the board through barrel
        jack (Vin). It is required to connect both USB0 and DEBUG USB to PC.

	https://www.microchip.com/en-us/development-tool/ea14v17a

*	Ensure MPLAB X Path is set in File -> Preference under System Settings. This helps
	* To program the Usecase prototyping kit by TPDS
	* To open the embedded project of the Usecase

*	Note that ~/.trustplatform/ pic32ck_sg01_provisioning’ is the Usecase working directory. It contains the resources(Firmware MetaData Tool) rquired for the use case and resources generated during transaction diagram execution.

   	* ~ indicates home directory.
	* Windows home directory is \user\username
	* Mac home directory is /users/username
	    Most Linux/Unix home directory is /home/username

Post Usecase transaction Steps
----
•	Log from the HSM provisioning and state of secure boot can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

