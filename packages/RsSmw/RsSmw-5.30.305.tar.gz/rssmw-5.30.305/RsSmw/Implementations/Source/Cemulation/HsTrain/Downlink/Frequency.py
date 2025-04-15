from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DOWNlink:FREQuency:STATe \n
		Snippet: value: bool = driver.source.cemulation.hsTrain.downlink.frequency.get_state() \n
		No command help available \n
			:return: hst_dl_freq_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:DOWNlink:FREQuency:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, hst_dl_freq_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DOWNlink:FREQuency:STATe \n
		Snippet: driver.source.cemulation.hsTrain.downlink.frequency.set_state(hst_dl_freq_state = False) \n
		No command help available \n
			:param hst_dl_freq_state: No help available
		"""
		param = Conversions.bool_to_str(hst_dl_freq_state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:DOWNlink:FREQuency:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DOWNlink:FREQuency \n
		Snippet: value: float = driver.source.cemulation.hsTrain.downlink.frequency.get_value() \n
		No command help available \n
			:return: hst_dl_freq: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:HSTRain:DOWNlink:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, hst_dl_freq: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:HSTRain:DOWNlink:FREQuency \n
		Snippet: driver.source.cemulation.hsTrain.downlink.frequency.set_value(hst_dl_freq = 1.0) \n
		No command help available \n
			:param hst_dl_freq: No help available
		"""
		param = Conversions.decimal_value_to_str(hst_dl_freq)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:HSTRain:DOWNlink:FREQuency {param}')
