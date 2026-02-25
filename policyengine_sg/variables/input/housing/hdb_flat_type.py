from policyengine_sg.model_api import *


class HDBFlatType(Enum):
    ONE_ROOM = "1-room"
    TWO_ROOM = "2-room"
    THREE_ROOM = "3-room"
    FOUR_ROOM = "4-room"
    FIVE_ROOM = "5-room"
    EXECUTIVE = "Executive"
    NON_HDB = "Non-HDB"


class hdb_flat_type(Variable):
    value_type = Enum
    possible_values = HDBFlatType
    default_value = HDBFlatType.FOUR_ROOM
    entity = Household
    label = "HDB flat type"
    definition_period = YEAR
