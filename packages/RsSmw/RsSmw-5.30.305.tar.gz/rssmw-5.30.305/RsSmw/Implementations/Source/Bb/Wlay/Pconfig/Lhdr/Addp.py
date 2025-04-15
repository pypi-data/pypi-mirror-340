from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddpCls:
	"""Addp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("addp", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:ADDP:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.lhdr.addp.get_state() \n
		If PPDU aggregation is active, activates an additional PPDU. See [:SOURce<hw>]:BB:WLAY:PCONfig:LHDR:PAGR:STATe. \n
			:return: addi_ppdu: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:ADDP:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, addi_ppdu: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:ADDP:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.lhdr.addp.set_state(addi_ppdu = False) \n
		If PPDU aggregation is active, activates an additional PPDU. See [:SOURce<hw>]:BB:WLAY:PCONfig:LHDR:PAGR:STATe. \n
			:param addi_ppdu: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(addi_ppdu)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:ADDP:STATe {param}')
