# STM32 Flasher

## RU

### Описание
**STM32 Flasher** - утилита для работы с кастомным загрузчиком микроконтроллера **STM32F407VET6**, выполняющим обновление программного обеспечения через интерфейс **Ethernet** в проектах, использующих
сетевой контроллер **W5500 (WizNet)**.

Программа предназначена для записи прошивки в устройство, в котором используется указанный загрузчик.

### Совместимость
- **Платформы:** Windows 10/11, Ubuntu 22.04
- **Требования для запуска:** Python **>= 3.13**, PyQt **>= 6.10.2**
- **Совместимость версий:** **STM32Flasher 0.5.3** совместим с **bootloader_stm32f407 0.2.0**

### Запуск
- Убедитесь, что у вас установлена последняя необходимая версия PyQt6
- **Windows 10/11:** Запустите утилиту двойным нажатием мыши по файлу `flasher.py`, либо введите название файла `flasher.py` в терминале, запущенном в директории программы (Python должен быть добавлен в системную переменную **PATH**).
- **Ubuntu 22.04:** Введите команду `python3 flasher.py` в терминале, запущенном в директории программы.

### Документация
Подробная иснструкция по использованию программы находится в Wiki проекта.

### Ссылки
Репозиторий загрузчика: https://github.com/smalltown-boy/bootloader_stm32f407  


## EN

### Description
**STM32 Flasher** is a utility for working with a custom bootloader for the **STM32F407VET6** microcontroller, which performs firmware updates over the **Ethernet** interface in projects using the **W5500 (WizNet)** Ethernet controller.

The program is intended for flashing firmware to a device that uses the specified bootloader.

### Compatibility
- **Platforms:** Windows 10/11, Ubuntu 22.04
- **Runtime requirements:** Python **>= 3.13**, PyQt **>= 6.10.2**
- **Version compatibility:** **STM32 Flasher 0.5.3** is compatible with **bootloader_stm32f407 0.2.0**

### Running
- Make sure you have the latest required version of PyQt6 installed.
- **Windows 10/11:** Launch the utility by double-clicking `flasher.py`, or type `flasher.py` in a terminal opened in the program directory (Python must be added to the system **PATH** environment variable).
- **Ubuntu 22.04:** Run `python3 flasher.py` in a terminal opened in the program directory.

### Documentation
A detailed user guide is available in the project Wiki.

### Links
Bootloader repository: https://github.com/smalltown-boy/bootloader_stm32f407