from policyengine_sg.model_api import *


class total_personal_reliefs(Variable):
    value_type = float
    entity = Person
    label = "Total personal reliefs"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs
        reliefs = add(
            person,
            period,
            [
                "earned_income_relief",
                "cpf_relief",
                "spouse_relief",
                "child_relief",
                "parent_relief",
                "nsman_relief",
                "srs_relief",
                "cpf_top_up_relief",
                "course_fees_relief",
                "life_insurance_relief",
            ],
        )
        return min_(reliefs, p.cap)
