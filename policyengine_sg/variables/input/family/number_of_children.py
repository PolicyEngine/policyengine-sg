from policyengine_sg.model_api import *


class number_of_children(Variable):
    value_type = int
    entity = Person
    label = "Number of qualifying children"
    definition_period = YEAR
    default_value = 0
