from policyengine_sg.model_api import *
from policyengine_sg.variables.input.education.school_level import (
    SchoolLevel,
)


class edusave_contribution(Variable):
    value_type = float
    entity = Person
    label = "Annual Edusave account contribution"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.moe.gov.sg/" "financial-matters/edusave-account/overview"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.moe.edusave
        citizen = person("is_citizen", period)
        level = person("school_level", period)
        amount = select(
            [
                level == SchoolLevel.PRIMARY,
                level == SchoolLevel.SECONDARY,
            ],
            [p.primary, p.secondary],
            default=0,
        )
        return where(citizen, amount, 0)
