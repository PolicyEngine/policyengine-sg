from policyengine_sg.model_api import *


class comcare_smta_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for ComCare Short-to-Medium-Term Assistance"
    definition_period = YEAR
    reference = (
        "https://www.msf.gov.sg/what-we-do/comcare",
        "https://supportgowhere.life.gov.sg/schemes/"
        "COMCARE-SMTA/comcare-short-to-medium-term"
        "-assistance-smta",
    )

    def formula(person, period, parameters):
        # SMTA uses the same eligibility criteria as
        # general ComCare. Benefit amounts are determined
        # by caseworker assessment, not a fixed formula.
        return person("comcare_eligible", period)
