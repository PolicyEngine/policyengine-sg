from policyengine_sg.model_api import *


class is_pr(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is a Singapore" " permanent resident"
    definition_period = YEAR
    default_value = False
