from policyengine_sg.model_api import *


class has_child_under_16(Variable):
    value_type = bool
    entity = Person
    label = "Has a Singapore Citizen child under age 16 in household"
    definition_period = YEAR
    default_value = False
