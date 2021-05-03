import dataclasses


@dataclasses.dataclass
class MigratedCountingDTO:
    success: int
    error: int
