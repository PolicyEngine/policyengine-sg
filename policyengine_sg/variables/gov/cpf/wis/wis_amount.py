from policyengine_sg.model_api import *


class wis_amount(Variable):
    value_type = float
    entity = Person
    label = "Workfare Income Supplement amount"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/member/"
        "growing-your-savings/"
        "government-support/"
        "workfare-income-supplement"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.wis
        eligible = person("wis_eligible", period)
        age = person("age", period)
        disabled = person("is_disabled", period)
        amount = select(
            [age < 35, age < 45, age < 60],
            [
                p.max_annual.age_30_to_34,
                p.max_annual.age_35_to_44,
                p.max_annual.age_45_to_59,
            ],
            default=(p.max_annual.age_60_and_above),
        )
        amount = where(
            disabled,
            p.max_annual.age_60_and_above,
            amount,
        )
        return where(eligible, amount, 0)
