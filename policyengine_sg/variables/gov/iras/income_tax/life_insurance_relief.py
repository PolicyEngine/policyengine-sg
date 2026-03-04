from policyengine_sg.model_api import *


class life_insurance_relief(Variable):
    value_type = float
    entity = Person
    label = "Life insurance relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "life-insurance-relief"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.life_insurance
        premium = person("life_insurance_premium", period)
        cpf = person("cpf_employee_contribution", period)
        available = max_(p.cap - cpf, 0)
        return min_(premium, available)
