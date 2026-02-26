from policyengine_sg.model_api import *


class wis_cash(Variable):
    value_type = float
    entity = Person
    label = "WIS cash component"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.cpf.gov.sg/member/growing-your-savings/government-support/workfare-income-supplement"

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.wis
        total = person("wis_amount", period)
        return total * p.cash_share
