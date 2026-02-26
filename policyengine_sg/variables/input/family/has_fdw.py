from policyengine_sg.model_api import *


class has_fdw(Variable):
    value_type = bool
    entity = Person
    label = "Employs a foreign domestic worker"
    definition_period = YEAR
    default_value = False
