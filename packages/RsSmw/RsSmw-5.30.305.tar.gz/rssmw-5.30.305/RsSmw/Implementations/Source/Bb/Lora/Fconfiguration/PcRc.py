from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcRcCls:
	"""PcRc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcRc", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:PCRC:STATe \n
		Snippet: value: bool = driver.source.bb.lora.fconfiguration.pcRc.get_state() \n
		Activates a cyclic redundancy check (CRC) of the payload. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:PCRC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:PCRC:STATe \n
		Snippet: driver.source.bb.lora.fconfiguration.pcRc.set_state(state = False) \n
		Activates a cyclic redundancy check (CRC) of the payload. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:PCRC:STATe {param}')
