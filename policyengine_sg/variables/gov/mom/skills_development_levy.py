from policyengine_sg.model_api import *


class skills_development_levy(Variable):
    value_type = float
    entity = Person
    label = "Skills Development Levy"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/employer/employer-obligations/skills-development-levy"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.mom.sdl
        income = person("employment_income", period)
        monthly = income / 12
        levy = monthly * p.rate
        capped = max_(min_(levy, p.maximum), p.minimum)
        return capped * 12
