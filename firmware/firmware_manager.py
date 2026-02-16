from abc import ABC, abstractmethod
from pathlib import Path
from intelhex import IntelHex
from elftools.elf.elffile import ELFFile

class FirmwareManager(ABC):
    def __init__(self, firmware_path: str, settings):
        self.firmware_path = firmware_path
        self.settings = settings
        self.base_address = None
        self.binary = None
        
    @abstractmethod
    def convert_to_binary(self) -> bytes:
        pass
        
    @staticmethod
    def create(path: str, settings):    
        ext = Path(path).suffix.lower()

        if ext == ".bin":
            return BinFile(path, settings)
        elif ext == ".hex":
            return HexFile(path, settings)
        elif ext == ".elf":
            return ElfFile(path, settings)
        else:
            raise ValueError("Unsupported firmware format")
            
    def validate_stm32_vector_table(self):
        if len(self.binary) < 8:
            raise ValueError("Firmware too small")

        sp = int.from_bytes(self.binary[0:4], "little")
        reset = int.from_bytes(self.binary[4:8], "little")
        
        ram_start = self.settings.ram_start
        ram_end = self.settings.ram_end

        flash_start = self.settings.flash_start
        flash_end = self.settings.flash_end

        if not (ram_start <= sp <= ram_end):
            raise ValueError(f"Invalid Stack Pointer: 0x{sp:08X}")

        if not (flash_start <= reset <= flash_end):
            raise ValueError(f"Invalid Reset_Handler: 0x{reset:08X}")

        return sp, reset
        
    
class BinFile(FirmwareManager):
    def convert_to_binary(self) -> bytes:
        with open(self.firmware_path, "rb") as f:
            self.binary = f.read()

        self.base_address = self.settings.flash_start
        return self.binary
        
class HexFile(FirmwareManager):
    def convert_to_binary(self) -> bytes:
        ih = IntelHex(self.firmware_path)

        start = ih.minaddr()
        end = ih.maxaddr()

        if start != self.settings.flash_start:
            raise ValueError(
                f"HEX base address 0x{start:08X} "
                f"does not match expected 0x{FLASH_BASE:08X}"
            )

        size = end - start + 1

        self.binary = ih.tobinarray(
            start=start,
            size=size
        ).tobytes()

        self.base_address = start
        return self.binary

class ElfFile(FirmwareManager):
    def convert_to_binary(self) -> bytes:
        segments = []

        flash_start = self.settings.flash_start
        flash_end = self.settings.flash_end
        max_fw_size = self.settings.flash_size * 1024
  
        with open(self.firmware_path, "rb") as f:
            elf = ELFFile(f)

            for segment in elf.iter_segments():
                if segment['p_type'] != 'PT_LOAD':
                    continue

                addr = segment['p_paddr']
                data = segment.data()

                # Нам нужен отлько flash сегмент
                if flash_start <= addr < flash_end:
                    segments.append((addr, data))

        if not segments:
            raise ValueError("No FLASH segments found in ELF")

        segments.sort(key=lambda x: x[0])

        start = segments[0][0]
        end = max(addr + len(data) for addr, data in segments)

        # Защита от переполнения flash в принципе
        if end > flash_end:
            raise ValueError("Firmware exceeds FLASH size")
            
        if start != flash_start:
            raise ValueError(
            f"ELF base address 0x{start:08X} "
            f"does not match expected 0x{FLASH_BASE:08X}"
        )
  
        size = end - start

        # Защита от переполнения. 480кБ - максимально допустимый размер загрузчика при использоваинии
        # моего бутлоадера
        if size > max_fw_size:
            raise ValueError(f"Firmware too large: {size} bytes")

        binary = bytearray([0xFF] * size)

        for addr, data in segments:
            offset = addr - start
            binary[offset:offset + len(data)] = data

        self.binary = bytes(binary)
        self.base_address = start

        return self.binary

