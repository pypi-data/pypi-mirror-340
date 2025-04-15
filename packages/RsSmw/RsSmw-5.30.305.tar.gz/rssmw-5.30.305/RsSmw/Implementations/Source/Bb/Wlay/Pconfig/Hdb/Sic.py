from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SicCls:
	"""Sic commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sic", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:SIC:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hdb.sic.get_state() \n
		If activated, applies superimposed code with LDPC codewords. \n
			:return: superimposed_cod: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:SIC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, superimposed_cod: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:SIC:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hdb.sic.set_state(superimposed_cod = False) \n
		If activated, applies superimposed code with LDPC codewords. \n
			:param superimposed_cod: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(superimposed_cod)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:SIC:STATe {param}')
