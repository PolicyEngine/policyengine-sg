from policyengine_sg.model_api import *


class earned_income_relief(Variable):
    value_type = float
    entity = Person
    label = "Earned income relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/earned-income-relief"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.earned_income
        age = person("age", period)
        disabled = person("is_disabled", period)
        earned = person("employment_income", period)
        se = person("self_employment_income", period)
        total_earned = earned + se

        normal_relief = select(
            [age < 55, age < 60],
            [p.below_55, p.age_55_to_59],
            default=p.age_60_and_above,
        )
        disability_relief = select(
            [age < 55, age < 60],
            [
                p.disability_below_55,
                p.disability_55_to_59,
            ],
            default=p.disability_60_and_above,
        )
        max_relief = where(disabled, disability_relief, normal_relief)
        return min_(max_relief, total_earned)
