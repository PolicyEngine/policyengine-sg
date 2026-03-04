from policyengine_sg.model_api import *


class BuyerProfile(Enum):
    CITIZEN_FIRST = "Citizen first property"
    CITIZEN_SECOND = "Citizen second property"
    CITIZEN_THIRD_AND_SUBSEQUENT = "Citizen third and subsequent property"
    PR_FIRST = "PR first property"
    PR_SECOND = "PR second property"
    PR_THIRD_AND_SUBSEQUENT = "PR third and subsequent property"
    FOREIGNER = "Foreigner"


class buyer_profile(Variable):
    value_type = Enum
    possible_values = BuyerProfile
    default_value = BuyerProfile.CITIZEN_FIRST
    entity = Household
    label = "Property buyer profile for stamp duty"
    definition_period = YEAR
