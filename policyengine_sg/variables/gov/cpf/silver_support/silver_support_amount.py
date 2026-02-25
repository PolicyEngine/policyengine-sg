from policyengine_sg.model_api import *


class silver_support_amount(Variable):
    value_type = float
    entity = Person
    label = "Silver Support annual payment"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/member/"
        "retirement-income/"
        "government-support/"
        "silver-support-scheme"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.silver_support
        eligible = person("silver_support_eligible", period)
        quarterly = p.quarterly.three_room_higher
        return where(
            eligible,
            quarterly * p.quarters_per_year,
            0,
        )
