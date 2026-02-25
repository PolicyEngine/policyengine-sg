from policyengine_sg.model_api import *


class spouse_is_disabled(Variable):
    value_type = bool
    entity = Person
    label = "Whether the spouse has a disability"
    definition_period = YEAR
    default_value = False
