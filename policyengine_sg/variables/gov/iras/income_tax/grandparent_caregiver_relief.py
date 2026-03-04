from policyengine_sg.model_api import *


class grandparent_caregiver_relief(Variable):
    value_type = float
    entity = Person
    label = "Grandparent caregiver relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "grandparent-caregiver-relief"
    )

    def formula(person, period, parameters):
        p = parameters(
            period
        ).gov.iras.income_tax.reliefs.grandparent_caregiver
        eligible = person("is_grandparent_caregiver", period)
        return where(eligible, p.amount, 0)
