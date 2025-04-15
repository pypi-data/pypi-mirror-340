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
		"""SCPI: [SOURce<HW>]:CEMulation:SPEed:UNIT \n
		Snippet: value: enums.UnitSpeed = driver.source.cemulation.speed.get_unit() \n
		No command help available \n
			:return: unit: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SPEed:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSpeed)

	def set_unit(self, unit: enums.UnitSpeed) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SPEed:UNIT \n
		Snippet: driver.source.cemulation.speed.set_unit(unit = enums.UnitSpeed.KMH) \n
		No command help available \n
			:param unit: No help available
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.UnitSpeed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SPEed:UNIT {param}')
