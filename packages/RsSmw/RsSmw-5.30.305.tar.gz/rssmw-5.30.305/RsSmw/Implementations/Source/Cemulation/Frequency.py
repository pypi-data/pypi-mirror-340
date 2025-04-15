from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_detect(self) -> enums.TmastConn:
		"""SCPI: [SOURce<HW>]:CEMulation:FREQuency:DETect \n
		Snippet: value: enums.TmastConn = driver.source.cemulation.frequency.get_detect() \n
		No command help available \n
			:return: detect_primary: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:FREQuency:DETect?')
		return Conversions.str_to_scalar_enum(response, enums.TmastConn)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:FREQuency \n
		Snippet: value: float = driver.source.cemulation.frequency.get_value() \n
		No command help available \n
			:return: frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:FREQuency \n
		Snippet: driver.source.cemulation.frequency.set_value(frequency = 1.0) \n
		No command help available \n
			:param frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:FREQuency {param}')
