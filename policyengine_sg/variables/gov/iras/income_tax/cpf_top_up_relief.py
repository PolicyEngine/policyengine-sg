from policyengine_sg.model_api import *


class cpf_top_up_relief(Variable):
    value_type = float
    entity = Person
    label = "CPF cash top-up relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/central-provident-"
        "fund-(cpf)-cash-top-up-relief"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.cpf_cash_top_up
        top_up = person("cpf_cash_top_up", period)
        return min_(top_up, p.self_amount)
