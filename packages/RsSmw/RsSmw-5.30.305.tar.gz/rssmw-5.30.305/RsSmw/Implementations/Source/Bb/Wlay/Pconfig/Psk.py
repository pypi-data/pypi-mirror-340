from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PskCls:
	"""Psk commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("psk", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:PSK:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.psk.get_state() \n
		Activates Pi/2-8PSK modulation. If activated, the bit in the Pi/2-8-PSK Applied field is 1. If deactivated, applies
		Pi/2-16QAM modulation. The bit in the Pi/2-8-PSK Applied field is 0. \n
			:return: psk_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:PSK:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, psk_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:PSK:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.psk.set_state(psk_state = False) \n
		Activates Pi/2-8PSK modulation. If activated, the bit in the Pi/2-8-PSK Applied field is 1. If deactivated, applies
		Pi/2-16QAM modulation. The bit in the Pi/2-8-PSK Applied field is 0. \n
			:param psk_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(psk_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:PSK:STATe {param}')
