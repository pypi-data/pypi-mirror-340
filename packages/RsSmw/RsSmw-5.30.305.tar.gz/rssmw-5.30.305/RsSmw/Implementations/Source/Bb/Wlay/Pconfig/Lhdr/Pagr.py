from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PagrCls:
	"""Pagr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pagr", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:PAGR:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.lhdr.pagr.get_state() \n
		Queries the PPDU aggregation state that is off. \n
			:return: ppdu_aggregate: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:PAGR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, ppdu_aggregate: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:PAGR:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.lhdr.pagr.set_state(ppdu_aggregate = False) \n
		Queries the PPDU aggregation state that is off. \n
			:param ppdu_aggregate: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(ppdu_aggregate)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:PAGR:STATe {param}')
