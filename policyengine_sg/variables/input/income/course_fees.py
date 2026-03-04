from policyengine_sg.model_api import *


class course_fees(Variable):
    value_type = float
    entity = Person
    label = "Qualifying course fees"
    unit = SGD
    definition_period = YEAR
    default_value = 0
