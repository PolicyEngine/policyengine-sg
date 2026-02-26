from policyengine_sg.model_api import *


class is_owner_occupied(Variable):
    value_type = bool
    entity = Household
    label = "Whether the property is" " owner-occupied"
    definition_period = YEAR
    default_value = True
