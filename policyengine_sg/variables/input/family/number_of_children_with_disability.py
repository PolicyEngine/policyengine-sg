from policyengine_sg.model_api import *


class number_of_children_with_disability(Variable):
    value_type = int
    entity = Person
    label = "Number of qualifying children" " with disability"
    definition_period = YEAR
    default_value = 0
