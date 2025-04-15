from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionCls:
	"""Correction commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correction", core, parent)

	def get_file(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice:CORRection:FILE \n
		Snippet: value: str = driver.source.efrontend.extDevice.correction.get_file() \n
		Selects an existing correction file, e.g. to compensate for cable losses. Selectable files have file extension *.s2p or *.
		uco. \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:EXTDevice:CORRection:FILE?')
		return trim_str_response(response)

	def set_file(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice:CORRection:FILE \n
		Snippet: driver.source.efrontend.extDevice.correction.set_file(filename = 'abc') \n
		Selects an existing correction file, e.g. to compensate for cable losses. Selectable files have file extension *.s2p or *.
		uco. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:EXTDevice:CORRection:FILE {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice:CORRection:STATe \n
		Snippet: value: bool = driver.source.efrontend.extDevice.correction.get_state() \n
		Activates correction of the RF signal for different RF signal frequencies. Activation requires loading of a valid
		correction file. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:EXTDevice:CORRection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice:CORRection:STATe \n
		Snippet: driver.source.efrontend.extDevice.correction.set_state(state = False) \n
		Activates correction of the RF signal for different RF signal frequencies. Activation requires loading of a valid
		correction file. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:EXTDevice:CORRection:STATe {param}')
