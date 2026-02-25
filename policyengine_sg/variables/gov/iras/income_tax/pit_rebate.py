from policyengine_sg.model_api import *


class pit_rebate(Variable):
    value_type = float
    entity = Person
    label = "Personal income tax rebate"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "personal-income-tax-rebate"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.rebates
        tax = person("income_tax_before_rebate", period)
        rebate = tax * p.pit_rebate_rate
        return min_(rebate, p.pit_rebate_cap)
