from enum import IntEnum


class AddIssueStatus(IntEnum):
    SUCCESS = 1
    INVALID_CATEGORY = -1
    DUPLICATE = -2
    DATABASE_ERROR = -3