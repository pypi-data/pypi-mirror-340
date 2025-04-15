# Trust Platform Design Suite Usecase Help – Immutable Boot

This document helps to understand Pre and Post steps of Usecase transaction diagram.

## Setup requirements
 - [PIC32CXSG41 Curiosity Ultra](https://www.microchip.com/en-us/development-tool/EV06X38A)
 - [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide)

## Pre Usecase transaction Steps
 - Connect PIC32CXSG41 Curiosity board to PC running Trust Platform Design Suite. It is required to connect DEBUG USB to PC.
 - Ensure *MPLAB X IDE Path* is set in *File* -> *Preference* under *System Settings*. This helps
	- To program the Usecase prototyping kit by TPDS
	- To open the embedded project of the Usecase
 - Note that *~/.trustplatform/ pic32cxsg41_immutable_boot* is the **Usecase working directory**. It contains the resources generated during transaction diagram execution.
 - ~ indicates home directory.
	- Windows home directory is \user\username
	- Mac home directory is /users/username
	    Most Linux/Unix home directory is /home/username

## Post Usecase transaction Steps
On completing Usecase steps execution on TPDS, the combined hex file is programmed to development kit. it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

 - Log from the combined hex file can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1
