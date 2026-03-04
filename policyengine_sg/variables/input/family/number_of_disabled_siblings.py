from policyengine_sg.model_api import *


class number_of_disabled_siblings(Variable):
    value_type = int
    entity = Person
    label = "Number of disabled siblings"
    definition_period = YEAR
    default_value = 0
