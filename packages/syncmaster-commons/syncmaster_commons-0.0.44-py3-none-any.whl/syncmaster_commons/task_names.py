from enum import Enum


class TaskNames(Enum):
    """
    TaskNames is an enum that defines the task names for the syncmaster library.
    """
    PITCH_SALES = "Pitch Sales"
    FOLLOW_UP = "Follow Up"
    CRM_UPDATE= "CRM Update"

    def __str__(self):
        return self.value

   