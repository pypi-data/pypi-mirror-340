from enum import Enum

class EnDataPointValueTypeDTO(str, Enum):
    FLUX = "Flux"
    INTEGRATED = "Integrated"

    def __str__(self) -> str:
        return str(self.value)
