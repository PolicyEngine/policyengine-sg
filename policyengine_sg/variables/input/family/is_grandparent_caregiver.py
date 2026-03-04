from policyengine_sg.model_api import *


class is_grandparent_caregiver(Variable):
    value_type = bool
    entity = Person
    label = (
        "Whether a working mother uses grandparent"
        " caregiver for child aged 12 or below"
    )
    definition_period = YEAR
    default_value = False
