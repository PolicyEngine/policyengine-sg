from policyengine_sg.model_api import *


class number_of_children_in_childcare(Variable):
    value_type = int
    entity = Person
    label = (
        "Number of children enrolled in licensed"
        " childcare (age 18 months to 6 years)"
    )
    definition_period = YEAR
    default_value = 0
