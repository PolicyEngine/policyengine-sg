from policyengine_sg.model_api import *


class monthly_scc_charge(Variable):
    value_type = float
    entity = Household
    label = "Monthly service and conservancy charge (S&CC)"
    unit = SGD
    definition_period = YEAR
    default_value = 0
