from policyengine_sg.model_api import *


class nsman_relief(Variable):
    value_type = float
    entity = Person
    label = "NSman relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/nsman-relief-"
        "(self-wife-and-parent)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.nsman
        is_nsman = person("is_nsman", period)
        return where(is_nsman, p.active, 0)
