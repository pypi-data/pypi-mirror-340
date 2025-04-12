from barril.units import Scalar

from alfasim_score.units import DENSITY_UNIT
from alfasim_score.units import DIAMETER_UNIT
from alfasim_score.units import FRACTION_UNIT
from alfasim_score.units import HEAT_TRANSFER_COEFFICIENT_UNIT
from alfasim_score.units import LENGTH_UNIT
from alfasim_score.units import MASS_FLOW_RATE_UNIT
from alfasim_score.units import PRESSURE_UNIT
from alfasim_score.units import ROUGHNESS_UNIT
from alfasim_score.units import STD_VOLUMETRIC_FLOW_RATE_UNIT

WELLBORE_NAME = "WELLBORE"
WELLBORE_TOP_NODE_NAME = "WELLBORE_TOP_NODE"
WELLBORE_BOTTOM_NODE_NAME = "WELLBORE_BOTTOM_NODE"
ANNULUS_TOP_NODE_NAME = "WELLBORE_ANNULUS_TOP_NODE"
GAS_LIFT_MASS_NODE_NAME = "GAS_LIFT_MASS_NODE"
CEMENT_NAME = "cement"
GAS_LIFT_VALVE_NAME = "GAS_LIFT_VALVE"

# prefixes used to identify the class of material for the APB plugin (ALFAsim)
CEMENT_PREFIX = "CM_"
FORMATION_PREFIX = "FC_"

ROCK_DEFAULT_ROUGHNESS = Scalar(0.1, ROUGHNESS_UNIT)
ROCK_DEFAULT_HEAT_TRANSFER_COEFFICIENT = Scalar(1000.0, HEAT_TRANSFER_COEFFICIENT_UNIT)
CASING_DEFAULT_ROUGHNESS = Scalar(0.05, ROUGHNESS_UNIT)
TUBING_DEFAULT_ROUGHNESS = Scalar(0.05, ROUGHNESS_UNIT)

REFERENCE_VERTICAL_COORDINATE = Scalar(0.0, LENGTH_UNIT, "length")

# this default fluid name for packer and fluid above filler
FLUID_DEFAULT_NAME = "fluid_default"

# nodes data
BASE_PVT_TABLE_NAME = "base"
GAS_LIFT_PVT_TABLE_NAME = "gas_lift"
NULL_VOLUMETRIC_FLOW_RATE = Scalar(0.0, STD_VOLUMETRIC_FLOW_RATE_UNIT)
NULL_MASS_FLOW_RATE = Scalar(0.0, MASS_FLOW_RATE_UNIT)

AIR_DENSITY_STANDARD = Scalar(1.225, DENSITY_UNIT)
WATER_DENSITY_STANDARD = Scalar(999.016, DENSITY_UNIT)

# default values used in the context of black-oil models
H2S_MOLAR_FRACTION_DEFAULT = Scalar(0.0, FRACTION_UNIT)
CO2_MOLAR_FRACTION_DEFAULT = Scalar(0.0, FRACTION_UNIT)

# gas lift default values
GAS_LIFT_VALVE_DEFAULT_DIAMETER = Scalar(0.25, DIAMETER_UNIT, "diameter")
GAS_LIFT_VALVE_DEFAULT_DISCHARGE = Scalar(0.826, FRACTION_UNIT)
GAS_LIFT_VALVE_DEFAULT_DELTA_P_MIN = Scalar(0.0, PRESSURE_UNIT)

# numerical and time options default values
MAXIMUM_TIMESTEP_CHANGE_FACTOR = 1.2
NUMERICAL_TOLERANCE = 1.0e-3
INITIAL_TIMESTEP = Scalar(0.1, "s")
MINIMUM_TIMESTEP = Scalar(1.0e-4, "s")
MAXIMUM_TIMESTEP = Scalar(2.0, "s")

# tolerance of depth to be considered an active annulus
ANNULUS_DEPTH_TOLERANCE = Scalar(10.0, LENGTH_UNIT)

# set default value for annulus for the plugin APB
# there is no such option in the SCORE input so use this default value
HAS_FLUID_RETURN = True

# total number of walls in the output
TOTAL_WALLS = 6
