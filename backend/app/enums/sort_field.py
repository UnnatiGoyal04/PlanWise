from enum import Enum

class SortField(str, Enum):
    TITLE = "title"
    PRIORITY = "priority"
    ESTIMATED_HOURS = "estimated_hours"