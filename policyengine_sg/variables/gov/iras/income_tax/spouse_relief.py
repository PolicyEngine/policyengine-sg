from policyengine_sg.model_api import *


class spouse_relief(Variable):
    value_type = float
    entity = Person
    label = "Spouse relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/spouse-relief-"
        "spouse-relief-(disability)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.spouse
        married = person("is_married", period)
        spouse_disabled = person("spouse_is_disabled", period)
        return where(
            ~married,
            0,
            where(
                spouse_disabled,
                p.disability_amount,
                p.amount,
            ),
        )
