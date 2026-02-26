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
        p = parameters(period).gov.iras.income_tax.reliefs
        married = person("is_married", period)
        spouse_disabled = person("spouse_is_disabled", period)
        spouse_inc = person("spouse_income", period)
        qualifies = married & (spouse_inc <= p.dependant_income_threshold)
        return where(
            ~qualifies,
            0,
            where(
                spouse_disabled,
                p.spouse.disability_amount,
                p.spouse.amount,
            ),
        )
