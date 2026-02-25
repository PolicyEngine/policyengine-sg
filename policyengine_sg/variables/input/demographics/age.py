from policyengine_sg.model_api import *


class age(Variable):
    value_type = int
    entity = Person
    label = "Age"
    definition_period = YEAR
    default_value = 0
