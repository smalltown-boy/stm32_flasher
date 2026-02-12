from abc import ABC, abstractmethod
from pathlib import Path
from intelhex import IntelHex
from elftools.elf.elffile import ELFFile

FLASH_BASE = 0x08008000

class FirmwareManager(ABC):
    def __init__(self, firmware_path: str):
        self.firmware_path = firmware_path
        self.base_address = None
        self.binary = None
        
    @abstractmethod
    def convert_to_binary(self) -> bytes:
        pass
        
    @staticmethod
    def create(path: str):
        ext = Path(path).suffix.lower()

        if ext == ".bin":
            return BinFile(path)
        elif ext == ".hex":
            return HexFile(path)
        elif ext == ".elf":
            return ElfFile(path)
        else:
            raise ValueError("Unsupported firmware format")
            
    def validate_stm32_vector_table(self):
        """
        Что мы вообще ищем:
        1. Первое слово — SP в RAM (0x200xxxxx)
        2. Второе словоd — Reset_Handler во FLASH
        """
        if len(self.binary) < 8:
            raise ValueError("Firmware too small")

        sp = int.from_bytes(self.binary[0:4], "little")
        reset = int.from_bytes(self.binary[4:8], "little")

        if not (0x20000000 <= sp <= 0x20050000):
            raise ValueError(f"Invalid Stack Pointer: 0x{sp:08X}")

        if not (FLASH_BASE <= reset <= 0x08100000):
            raise ValueError(f"Invalid Reset_Handler: 0x{reset:08X}")

        return sp, reset
        
    
class BinFile(FirmwareFile):
    def convert_to_binary(self) -> bytes:
        with open(self.firmware_path, "rb") as f:
            self.binary = f.read()

        self.base_address = FLASH_BASE
        return self.binary
        
class HexFile(FirmwareManager):
    def convert(self) -> bytes:
        ih = IntelHex(self.firmware_path)

        start = ih.minaddr()
        end = ih.maxaddr()

        if start != FLASH_BASE:
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
    def convert(self) -> bytes:
        segments = []

        with open(self.firmware_path, "rb") as f:
            elf = ELFFile(f)

            for segment in elf.iter_segments():
                if segment['p_type'] == 'PT_LOAD':
                    addr = segment['p_paddr']
                    data = segment.data()
                    segments.append((addr, data))

        if not segments:
            raise ValueError("No loadable segments found")

        segments.sort(key=lambda x: x[0])

        start = segments[0][0]

        if start != FLASH_BASE:
            raise ValueError(
                f"ELF base address 0x{start:08X} "
                f"does not match expected 0x{FLASH_BASE:08X}"
            )

        end = max(addr + len(data) for addr, data in segments)
        size = end - start

        binary = bytearray([0xFF] * size)

        for addr, data in segments:
            offset = addr - start
            binary[offset:offset + len(data)] = data

        self.binary = bytes(binary)
        self.base_address = start

        return self.binary
