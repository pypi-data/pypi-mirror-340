from dataclasses import dataclass


@dataclass
class SignalRead:
    on: bool
    wavelength: int
