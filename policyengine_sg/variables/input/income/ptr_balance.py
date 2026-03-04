from policyengine_sg.model_api import *


class ptr_balance(Variable):
    value_type = float
    entity = Person
    label = (
        "Remaining parenthood tax rebate balance"
        " carried forward from prior years"
    )
    unit = SGD
    definition_period = YEAR
    default_value = 0
