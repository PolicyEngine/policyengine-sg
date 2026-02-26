from policyengine_sg.model_api import *


class cda_first_step_grant(Variable):
    value_type = float
    entity = Person
    label = "CDA First Step Grant total entitlement"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.life.gov.sg/family-parenting/"
        "benefits-support/baby-bonus-scheme/cda"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.msf.cda
        n = person("number_of_children", period)
        citizen = person("is_citizen", period)
        boundary = p.child_tier_boundary
        first_second = min_(n, boundary) * p.first_step_first_second
        third_plus = max_(n - boundary, 0) * p.first_step_third_plus
        return where(citizen, first_second + third_plus, 0)
