from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpeedCls:
	"""Speed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("speed", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.UnitSpeed:
		"""SCPI: [SOURce<HW>]:FSIMulator:SPEed:UNIT \n
		Snippet: value: enums.UnitSpeed = driver.source.fsimulator.speed.get_unit() \n
		Sets the unit for the speed of a moving receiver. Note that this setting only changes the speed unit in local mode.
		To set the speed units via remote control set the unit after the speed value. \n
			:return: unit: MPS| KMH| MPH| NMPH
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:SPEed:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSpeed)

	def set_unit(self, unit: enums.UnitSpeed) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:SPEed:UNIT \n
		Snippet: driver.source.fsimulator.speed.set_unit(unit = enums.UnitSpeed.KMH) \n
		Sets the unit for the speed of a moving receiver. Note that this setting only changes the speed unit in local mode.
		To set the speed units via remote control set the unit after the speed value. \n
			:param unit: MPS| KMH| MPH| NMPH
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.UnitSpeed)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:SPEed:UNIT {param}')
