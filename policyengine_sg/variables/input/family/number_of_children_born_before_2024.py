from policyengine_sg.model_api import *


class number_of_children_born_before_2024(Variable):
    value_type = int
    entity = Person
    label = (
        "Number of qualifying children born or"
        " adopted before 1 January 2024"
    )
    definition_period = YEAR
    default_value = 0
