from policyengine_sg.model_api import *


class is_parent_of_nsman(Variable):
    value_type = bool
    entity = Person
    label = "Is parent of an NSman"
    definition_period = YEAR
    default_value = False
