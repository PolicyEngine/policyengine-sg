from policyengine_sg.model_api import *


class NsmanStatus(Enum):
    NOT_NSMAN = "Not NSman"
    ACTIVE = "Active"
    NON_ACTIVE = "Non-active"
    KEY_APPOINTMENT_ACTIVE = "Key appointment (active)"
    KEY_APPOINTMENT_NON_ACTIVE = "Key appointment (non-active)"


class nsman_status(Variable):
    value_type = Enum
    possible_values = NsmanStatus
    default_value = NsmanStatus.NOT_NSMAN
    entity = Person
    label = "NSman status"
    definition_period = YEAR
