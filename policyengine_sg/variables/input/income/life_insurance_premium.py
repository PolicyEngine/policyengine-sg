from policyengine_sg.model_api import *


class life_insurance_premium(Variable):
    value_type = float
    entity = Person
    label = "Life insurance premiums paid"
    unit = SGD
    definition_period = YEAR
    default_value = 0
