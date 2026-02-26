from policyengine_sg.model_api import *


class is_citizen(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is a Singapore citizen"
    definition_period = YEAR
    default_value = True
