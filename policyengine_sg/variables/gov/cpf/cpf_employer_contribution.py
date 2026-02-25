from policyengine_sg.model_api import *


class cpf_employer_contribution(Variable):
    value_type = float
    entity = Person
    label = "CPF employer contribution"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/employer/"
        "employer-obligations/"
        "how-much-cpf-contributions-to-pay"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.contribution_rates.employer
        wc = parameters(period).gov.cpf.wage_ceiling
        age = person("age", period)
        income = person("employment_income", period)
        capped = min_(income, wc.annual_wage_ceiling)
        rate = select(
            [
                age <= 55,
                age <= 60,
                age <= 65,
                age <= 70,
            ],
            [
                p.age_55_and_below,
                p.above_55_to_60,
                p.above_60_to_65,
                p.above_65_to_70,
            ],
            default=p.above_70,
        )
        return capped * rate
