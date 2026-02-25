from policyengine_sg.model_api import *


class wmcr(Variable):
    value_type = float
    entity = Person
    label = "Working mother's child relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "working-mother's-child-relief-(wmcr)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.wmcr
        is_female = person("is_female", period)
        is_married = person("is_married", period)
        n_children = person("number_of_children", period)
        earned = person("employment_income", period) + person(
            "self_employment_income", period
        )
        has_earned = earned > 0
        eligible = is_female & is_married & has_earned
        first = min_(n_children, 1) * p.first_child
        second = min_(max_(n_children - 1, 0), 1) * p.second_child
        third_plus = max_(n_children - 2, 0) * (p.third_and_subsequent_child)
        return where(eligible, first + second + third_plus, 0)
