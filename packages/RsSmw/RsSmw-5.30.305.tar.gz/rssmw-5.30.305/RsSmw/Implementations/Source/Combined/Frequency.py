from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_start(self) -> float:
		"""SCPI: [SOURce<HW>]:COMBined:FREQuency:STARt \n
		Snippet: value: float = driver.source.combined.frequency.get_start() \n
		No command help available \n
			:return: comb_freq_start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, comb_freq_start: float) -> None:
		"""SCPI: [SOURce<HW>]:COMBined:FREQuency:STARt \n
		Snippet: driver.source.combined.frequency.set_start(comb_freq_start = 1.0) \n
		No command help available \n
			:param comb_freq_start: No help available
		"""
		param = Conversions.decimal_value_to_str(comb_freq_start)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""SCPI: [SOURce<HW>]:COMBined:FREQuency:STOP \n
		Snippet: value: float = driver.source.combined.frequency.get_stop() \n
		No command help available \n
			:return: comb_freq_stop: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, comb_freq_stop: float) -> None:
		"""SCPI: [SOURce<HW>]:COMBined:FREQuency:STOP \n
		Snippet: driver.source.combined.frequency.set_stop(comb_freq_stop = 1.0) \n
		No command help available \n
			:param comb_freq_stop: No help available
		"""
		param = Conversions.decimal_value_to_str(comb_freq_stop)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:FREQuency:STOP {param}')
