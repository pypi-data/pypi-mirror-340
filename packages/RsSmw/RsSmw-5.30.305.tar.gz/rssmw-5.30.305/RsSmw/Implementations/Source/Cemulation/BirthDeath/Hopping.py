from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HoppingCls:
	"""Hopping commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hopping", core, parent)

	def get_dwell(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:HOPPing:DWELl \n
		Snippet: value: float = driver.source.cemulation.birthDeath.hopping.get_dwell() \n
		No command help available \n
			:return: dwell: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:HOPPing:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:HOPPing:DWELl \n
		Snippet: driver.source.cemulation.birthDeath.hopping.set_dwell(dwell = 1.0) \n
		No command help available \n
			:param dwell: No help available
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:HOPPing:DWELl {param}')
