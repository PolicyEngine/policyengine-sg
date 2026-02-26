from policyengine_sg.model_api import *


class is_first_time_homebuyer(Variable):
    value_type = bool
    entity = Person
    label = (
        "Is a first-time homebuyer (never owned HDB or received housing grant)"
    )
    definition_period = YEAR
    default_value = False
