from policyengine_sg.model_api import *


class srs_contribution(Variable):
    value_type = float
    entity = Person
    label = "Supplementary Retirement Scheme" " contribution"
    unit = SGD
    definition_period = YEAR
    default_value = 0
