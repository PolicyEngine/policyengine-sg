from policyengine_sg.model_api import *


class is_disabled(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person has a disability"
    definition_period = YEAR
    default_value = False
