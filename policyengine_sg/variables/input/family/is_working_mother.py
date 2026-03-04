from policyengine_sg.model_api import *


class is_working_mother(Variable):
    value_type = bool
    entity = Person
    label = "Is a working mother (works at least 56 hours per month)"
    definition_period = YEAR
    default_value = False
