from policyengine_sg.model_api import *


class number_of_children_in_kindergarten(Variable):
    value_type = int
    entity = Person
    label = (
        "Number of children enrolled in an"
        " Anchor Operator or MOE kindergarten"
    )
    definition_period = YEAR
    default_value = 0
