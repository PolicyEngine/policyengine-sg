from policyengine_sg.model_api import *


class cpf_total_contribution(Variable):
    value_type = float
    entity = Person
    label = "Total CPF contribution"
    unit = SGD
    definition_period = YEAR
    adds = [
        "cpf_employee_contribution",
        "cpf_employer_contribution",
    ]
