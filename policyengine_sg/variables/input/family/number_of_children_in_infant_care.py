from policyengine_sg.model_api import *


class number_of_children_in_infant_care(Variable):
    value_type = int
    entity = Person
    label = (
        "Number of children enrolled in licensed"
        " infant care (age 2 to 18 months)"
    )
    definition_period = YEAR
    default_value = 0
