from policyengine_sg.model_api import *


class baby_bonus_cash_gift(Variable):
    value_type = float
    entity = Person
    label = "Baby Bonus Cash Gift total entitlement"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.life.gov.sg/family-parenting/"
        "benefits-support/baby-bonus-scheme"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.msf.baby_bonus
        n = person("number_of_children", period)
        married = person("is_married", period)
        citizen = person("is_citizen", period)
        first_second = min_(n, 2) * p.first_second_child
        third_plus = max_(n - 2, 0) * p.third_and_subsequent_child
        return where(
            married & citizen,
            first_second + third_plus,
            0,
        )
