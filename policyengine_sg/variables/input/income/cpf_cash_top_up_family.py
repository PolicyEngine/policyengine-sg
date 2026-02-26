from policyengine_sg.model_api import *


class cpf_cash_top_up_family(Variable):
    value_type = float
    entity = Person
    label = "CPF cash top-up amount for family members'" " retirement accounts"
    unit = SGD
    definition_period = YEAR
    default_value = 0
