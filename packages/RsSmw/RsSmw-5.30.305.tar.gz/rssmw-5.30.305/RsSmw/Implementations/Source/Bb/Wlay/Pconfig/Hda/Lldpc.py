from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LldpcCls:
	"""Lldpc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lldpc", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:LLDPc:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.lldpc.get_state() \n
		Activates long low-density parity-check (LDPC) codewords. If disabled, the firmware uses short LDPC codewords. \n
			:return: lpdc: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:LLDPc:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, lpdc: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:LLDPc:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.lldpc.set_state(lpdc = False) \n
		Activates long low-density parity-check (LDPC) codewords. If disabled, the firmware uses short LDPC codewords. \n
			:param lpdc: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(lpdc)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:LLDPc:STATe {param}')
