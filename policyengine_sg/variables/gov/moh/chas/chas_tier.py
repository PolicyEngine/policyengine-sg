from policyengine_sg.model_api import *


class CHASTier(Enum):
    NOT_ELIGIBLE = "Not eligible"
    GREEN = "Green"
    ORANGE = "Orange"
    BLUE = "Blue"


class chas_tier(Variable):
    value_type = Enum
    possible_values = CHASTier
    default_value = CHASTier.NOT_ELIGIBLE
    entity = Person
    label = "CHAS card tier"
    definition_period = YEAR
    reference = "https://www.chas.sg"

    def formula(person, period, parameters):
        p = parameters(period).gov.moh.chas
        citizen = person("is_citizen", period)
        pci = person("household_income_per_capita", period)
        return where(
            ~citizen,
            CHASTier.NOT_ELIGIBLE,
            where(
                pci <= p.blue_threshold,
                CHASTier.BLUE,
                where(
                    pci <= p.orange_threshold,
                    CHASTier.ORANGE,
                    CHASTier.GREEN,
                ),
            ),
        )
