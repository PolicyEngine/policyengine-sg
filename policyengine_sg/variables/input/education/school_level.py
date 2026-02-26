from policyengine_sg.model_api import *


class SchoolLevel(Enum):
    NOT_IN_SCHOOL = "Not in school"
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    PRE_UNIVERSITY = "Pre-university"
    ITE = "ITE"
    POLYTECHNIC = "Polytechnic"


class school_level(Variable):
    value_type = Enum
    possible_values = SchoolLevel
    default_value = SchoolLevel.NOT_IN_SCHOOL
    entity = Person
    label = "School level"
    definition_period = YEAR
