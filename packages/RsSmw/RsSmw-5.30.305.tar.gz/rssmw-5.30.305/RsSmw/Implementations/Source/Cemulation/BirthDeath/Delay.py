from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def get_grid(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:DELay:GRID \n
		Snippet: value: float = driver.source.cemulation.birthDeath.delay.get_grid() \n
		No command help available \n
			:return: grid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:DELay:GRID?')
		return Conversions.str_to_float(response)

	def set_grid(self, grid: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:DELay:GRID \n
		Snippet: driver.source.cemulation.birthDeath.delay.set_grid(grid = 1.0) \n
		No command help available \n
			:param grid: No help available
		"""
		param = Conversions.decimal_value_to_str(grid)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:DELay:GRID {param}')

	def get_maximum(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:DELay:MAXimum \n
		Snippet: value: float = driver.source.cemulation.birthDeath.delay.get_maximum() \n
		No command help available \n
			:return: maximum: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:DELay:MAXimum?')
		return Conversions.str_to_float(response)

	def get_minimum(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:DELay:MINimum \n
		Snippet: value: float = driver.source.cemulation.birthDeath.delay.get_minimum() \n
		No command help available \n
			:return: minimum: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:DELay:MINimum?')
		return Conversions.str_to_float(response)

	def set_minimum(self, minimum: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:DELay:MINimum \n
		Snippet: driver.source.cemulation.birthDeath.delay.set_minimum(minimum = 1.0) \n
		No command help available \n
			:param minimum: No help available
		"""
		param = Conversions.decimal_value_to_str(minimum)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:DELay:MINimum {param}')
