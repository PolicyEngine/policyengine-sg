from policyengine_sg.model_api import *


class is_female(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is female"
    definition_period = YEAR
    default_value = False
