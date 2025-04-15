from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def get_maximum(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:DELay:MAXimum \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.delay.get_maximum() \n
		No command help available \n
			:return: maximum: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:DELay:MAXimum?')
		return Conversions.str_to_float(response)

	def set_maximum(self, maximum: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:DELay:MAXimum \n
		Snippet: driver.source.cemulation.tcInterferer.moving.delay.set_maximum(maximum = 1.0) \n
		No command help available \n
			:param maximum: No help available
		"""
		param = Conversions.decimal_value_to_str(maximum)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:DELay:MAXimum {param}')

	def get_minimum(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:DELay:MINimum \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.delay.get_minimum() \n
		No command help available \n
			:return: minimum: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:DELay:MINimum?')
		return Conversions.str_to_float(response)

	def set_minimum(self, minimum: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:DELay:MINimum \n
		Snippet: driver.source.cemulation.tcInterferer.moving.delay.set_minimum(minimum = 1.0) \n
		No command help available \n
			:param minimum: No help available
		"""
		param = Conversions.decimal_value_to_str(minimum)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:DELay:MINimum {param}')
