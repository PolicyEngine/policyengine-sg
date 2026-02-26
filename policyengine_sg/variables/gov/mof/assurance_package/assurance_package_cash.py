from policyengine_sg.model_api import *


class assurance_package_cash(Variable):
    value_type = float
    entity = Person
    label = "Assurance Package cash"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.govbenefits.gov.sg/"
        "about-us/assurance-package/am-i-eligible/"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.mof.assurance_package
        citizen = person("is_citizen", period)
        age = person("age", period)
        income = person("employment_income", period) + person(
            "self_employment_income", period
        )
        n_prop = person("number_of_properties", period)
        multi_prop = n_prop >= p.max_properties_for_lower_tier
        amount = where(
            multi_prop,
            p.higher_income,
            select(
                [
                    income <= p.income_threshold,
                    income <= p.income_threshold_upper,
                ],
                [p.low_income, p.middle_income],
                default=p.higher_income,
            ),
        )
        return where(citizen & (age >= p.age_minimum), amount, 0)
