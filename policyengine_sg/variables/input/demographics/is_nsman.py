from policyengine_sg.model_api import *


class is_nsman(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person performed" " national service activities"
    definition_period = YEAR
    default_value = False
