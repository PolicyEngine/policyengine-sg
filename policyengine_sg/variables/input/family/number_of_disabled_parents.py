from policyengine_sg.model_api import *


class number_of_disabled_parents(Variable):
    value_type = int
    entity = Person
    label = (
        "Number of dependant parents" " with disability living with taxpayer"
    )
    definition_period = YEAR
    default_value = 0
