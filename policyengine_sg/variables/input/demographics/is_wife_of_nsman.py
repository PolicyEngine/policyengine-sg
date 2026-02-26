from policyengine_sg.model_api import *


class is_wife_of_nsman(Variable):
    value_type = bool
    entity = Person
    label = "Is wife of an NSman"
    definition_period = YEAR
    default_value = False
