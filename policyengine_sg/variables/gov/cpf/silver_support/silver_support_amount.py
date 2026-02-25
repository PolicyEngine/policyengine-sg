from policyengine_sg.model_api import *
from policyengine_sg.variables.input.housing.hdb_flat_type import (
    HDBFlatType,
)


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
        flat_type = person.household("hdb_flat_type", period)
        income_pc = person("household_income_per_capita", period)
        monthly_pc = income_pc / 12
        is_higher = monthly_pc <= p.income_per_capita_higher_tier
        quarterly_higher = select(
            [
                (flat_type == HDBFlatType.ONE_ROOM)
                | (flat_type == HDBFlatType.TWO_ROOM),
                flat_type == HDBFlatType.THREE_ROOM,
                flat_type == HDBFlatType.FOUR_ROOM,
            ],
            [
                p.quarterly.one_two_room_higher,
                p.quarterly.three_room_higher,
                p.quarterly.four_room_higher,
            ],
            default=p.quarterly.five_room_higher,
        )
        quarterly_lower = select(
            [
                (flat_type == HDBFlatType.ONE_ROOM)
                | (flat_type == HDBFlatType.TWO_ROOM),
                flat_type == HDBFlatType.THREE_ROOM,
                flat_type == HDBFlatType.FOUR_ROOM,
            ],
            [
                p.quarterly.one_two_room_lower,
                p.quarterly.three_room_lower,
                p.quarterly.four_room_lower,
            ],
            default=p.quarterly.five_room_lower,
        )
        quarterly = where(is_higher, quarterly_higher, quarterly_lower)
        annual = quarterly * p.quarters_per_year
        return where(eligible, annual, 0)
