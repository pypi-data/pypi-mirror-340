from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhaseCls:
	"""Phase commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phase", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.UnitAngle:
		"""SCPI: [SOURce<HW>]:FSIMulator:PHASe:UNIT \n
		Snippet: value: enums.UnitAngle = driver.source.fsimulator.phase.get_unit() \n
		Sets the unit for the phase parameter, for example 'Const Phase'. Note that this setting only changes the speed unit in
		local mode. To set the speed units via remote control set the unit after the speed value. \n
			:return: fad_angle_unit: DEGree| DEGRee| RADian
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:PHASe:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitAngle)

	def set_unit(self, fad_angle_unit: enums.UnitAngle) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:PHASe:UNIT \n
		Snippet: driver.source.fsimulator.phase.set_unit(fad_angle_unit = enums.UnitAngle.DEGree) \n
		Sets the unit for the phase parameter, for example 'Const Phase'. Note that this setting only changes the speed unit in
		local mode. To set the speed units via remote control set the unit after the speed value. \n
			:param fad_angle_unit: DEGree| DEGRee| RADian
		"""
		param = Conversions.enum_scalar_to_str(fad_angle_unit, enums.UnitAngle)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:PHASe:UNIT {param}')
