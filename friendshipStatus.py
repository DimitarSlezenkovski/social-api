from enum import Enum


class Status(Enum):
    SENT = 1
    PENDING = 2
    ACCEPTED = 3
    CANCELED = 4
