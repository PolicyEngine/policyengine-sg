from policyengine_sg.model_api import *


class number_of_properties(Variable):
    value_type = int
    entity = Person
    label = "Number of properties owned"
    definition_period = YEAR
    default_value = 1
