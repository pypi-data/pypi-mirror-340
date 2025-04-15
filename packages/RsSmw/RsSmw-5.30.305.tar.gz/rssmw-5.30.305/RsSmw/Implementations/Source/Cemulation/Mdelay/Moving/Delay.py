from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def get_mean(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:DELay:MEAN \n
		Snippet: value: float = driver.source.cemulation.mdelay.moving.delay.get_mean() \n
		No command help available \n
			:return: mean: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:MOVing:DELay:MEAN?')
		return Conversions.str_to_float(response)

	def set_mean(self, mean: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:DELay:MEAN \n
		Snippet: driver.source.cemulation.mdelay.moving.delay.set_mean(mean = 1.0) \n
		No command help available \n
			:param mean: No help available
		"""
		param = Conversions.decimal_value_to_str(mean)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:MOVing:DELay:MEAN {param}')

	def get_variation(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:DELay:VARiation \n
		Snippet: value: float = driver.source.cemulation.mdelay.moving.delay.get_variation() \n
		No command help available \n
			:return: variation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:MOVing:DELay:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:DELay:VARiation \n
		Snippet: driver.source.cemulation.mdelay.moving.delay.set_variation(variation = 1.0) \n
		No command help available \n
			:param variation: No help available
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:MOVing:DELay:VARiation {param}')
