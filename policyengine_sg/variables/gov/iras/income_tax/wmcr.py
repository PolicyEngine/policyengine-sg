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
        n_total = person("number_of_children", period)
        n_pre = person("number_of_children_born_before_2024", period)
        n_post = max_(n_total - n_pre, 0)
        earned = person("employment_income", period) + person(
            "self_employment_income", period
        )
        has_earned = earned > 0
        eligible = is_female & is_married & has_earned
        # Pre-2024 children: percentage of earned income
        pre_rate = (
            min_(n_pre, 1) * p.first_child_rate
            + min_(max_(n_pre - 1, 0), 1) * p.second_child_rate
            + max_(n_pre - 2, 0) * p.third_and_subsequent_child_rate
        )
        pre_amount = earned * pre_rate
        # Post-2024 children: fixed amounts (by birth order
        # among post-2024 children only)
        post_first = min_(n_post, 1) * p.first_child
        post_second = min_(max_(n_post - 1, 0), 1) * p.second_child
        post_third = max_(n_post - 2, 0) * p.third_and_subsequent_child
        post_amount = post_first + post_second + post_third
        return where(eligible, pre_amount + post_amount, 0)
