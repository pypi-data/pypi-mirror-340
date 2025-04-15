from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DistanceCls:
	"""Distance commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("distance", core, parent)

	def get_minimum(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DISTance:MINimum \n
		Snippet: value: float = driver.source.cemulation.hsTrain.distance.get_minimum() \n
		No command help available \n
			:return: minimum: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:DISTance:MINimum?')
		return Conversions.str_to_float(response)

	def set_minimum(self, minimum: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DISTance:MINimum \n
		Snippet: driver.source.cemulation.hsTrain.distance.set_minimum(minimum = 1.0) \n
		No command help available \n
			:param minimum: No help available
		"""
		param = Conversions.decimal_value_to_str(minimum)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:DISTance:MINimum {param}')

	def get_start(self) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DISTance:STARt \n
		Snippet: value: int = driver.source.cemulation.hsTrain.distance.get_start() \n
		No command help available \n
			:return: start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:DISTance:STARt?')
		return Conversions.str_to_int(response)

	def set_start(self, start: int) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DISTance:STARt \n
		Snippet: driver.source.cemulation.hsTrain.distance.set_start(start = 1) \n
		No command help available \n
			:param start: No help available
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:DISTance:STARt {param}')
