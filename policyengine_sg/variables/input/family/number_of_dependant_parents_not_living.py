from policyengine_sg.model_api import *


class number_of_dependant_parents_not_living(Variable):
    value_type = int
    entity = Person
    label = "Number of dependant parents" " not living with taxpayer"
    definition_period = YEAR
    default_value = 0
