from policyengine_sg.model_api import *


class has_elderly_67_plus(Variable):
    value_type = bool
    entity = Person
    label = "Has a household member aged 67 or above"
    definition_period = YEAR
    default_value = False
