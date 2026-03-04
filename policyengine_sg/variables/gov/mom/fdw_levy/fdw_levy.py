from policyengine_sg.model_api import *


class fdw_levy(Variable):
    value_type = float
    entity = Person
    label = "Foreign domestic worker levy (annual)"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.mom.gov.sg/passes-and-permits/"
        "work-permit-for-foreign-domestic-worker/"
        "foreign-domestic-worker-levy/levy-concession"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.mom.fdw_levy
        has_worker = person("has_fdw", period)
        child = person("has_child_under_16", period)
        elderly = person("has_elderly_67_plus", period)
        disabled_member = person("is_disabled", period)
        concession = child | elderly | disabled_member
        monthly = where(concession, p.concessionary, p.standard)
        return where(has_worker, monthly * 12, 0)
