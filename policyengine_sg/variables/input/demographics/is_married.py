from policyengine_sg.model_api import *


class is_married(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is married"
    definition_period = YEAR
    default_value = False
