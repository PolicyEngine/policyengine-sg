from policyengine_sg.model_api import *


class ImmigrationStatus(Enum):
    CITIZEN = "Citizen"
    PERMANENT_RESIDENT = "Permanent Resident"
    FOREIGNER = "Foreigner"


class immigration_status(Variable):
    value_type = Enum
    possible_values = ImmigrationStatus
    default_value = ImmigrationStatus.CITIZEN
    entity = Person
    label = "Immigration status"
    definition_period = YEAR
