# Change history

All project changes are documented here.

## Version 0.6.2 (2026-02-12)

### New features

- Implemented a mechanism for creating a settings file
- Implemented a mechanism for reading settings from a file

### Fixes

- Updated the program version on the main form

## Version 0.6.1 (2026-02-12)

### In development

- Added the settings window form **ui_preferences.py**

### Fixes

-Updated the program version in the main form
-Fixed sections in the **CHANGELOG.md** and **CHANGELOG.ru.md** files

## Version 0.6.0 (2026-02-12)

### New features

- Added support for **.elf** and **.hex** formats
- Implemented display of brief file information
- For the **.elf** format, implemented checks for compliance with start and end addresses, as well as a check for exceeding the limits of available flash memory

### Fixes

- Updated the program version in the main form

## Version 0.5.4 (2026-02-12)

### In development

- Created the **firmware** directory with the **file_manager.py** file
- Created an abstract class **FirmwareManager** to work with different types of firmware
- Created a directory for temporary files: **temp**
- Added support for **.elf** and **.hex** formats in the file-opening function

### Fixes

- Changed the name of the firmware file opening button
- Updated the program version in the main form

## Version 0.5.3 (2026-02-11)

### Fixes

- Fixed the program version number on the main window (ui_main.py)
- Added the README.md file
- Added the LICENCE.md file

## Version 0.5.2 (2026-02-11)

### Fixes

- Fixed the font size for the parameter responsible for launching the main program after flashing the microcontroller

## Version 0.5.1 (2026-02-10)

### New features

- The user can choose whether the loader will switch to **main** after the flashing procedure is completed

### Version 0.5.0 (2026-02-10)

### New Features

- The connection button text now changes when the socket is opened
- The socket open button now also serves as a socket close button

## Version 0.4.0 (2026-02-10)

### Fixes

-Fixed a bug in the **save_history** method of the **HistoryManager** class
that prevented user-entered connection addresses from being saved correctly

-Added a call to **self.history.save_history()** in the
**on_connect_clicked** event of the **MainWindow** class

## Version 0.3.0 (2026-02-10)

### Changes

- Renamed the application to STM32 Flasher
- Added a Clear log button to the main window
- Added CHANGELOG.md and CHANGELOG.ru.md files

### New Features

Implemented a function to clear the log window

## Version 0.2.0 (2026-02-09)

### Changes

- The name of the program has been changed to **STM32 Flasher**
- The **Clear log** button has been added to the main window
- Added files **CHANGELOG.md** and **CHANGELOG.ru.md**

### New features

- The function of clearing the logging window has been implemented

## Version 0.1.0 (2026-02-08)

### New features

- Implemented the function of opening a UDP socket
- The function of connection parameter validation has been implemented
- The function of sending a command to clear the flash memory of the microcontroller has been implemented
- The function of sending firmware to the microcontroller loader has been implemented
- The opening function has been implemented.bin files
- Implemented the display of the firmware download process using the progress bar