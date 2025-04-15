from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZptCls:
	"""Zpt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zpt", core, parent)

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH0>]:[ZPRS<ST0>]:ZPT \n
		Snippet: value: str = driver.source.bb.eutra.downlink.csis.cell.zprs.zpt.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the parameter subframe configuration period TCSI-RS for CSI-RS with zero transmission power. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Zprs')
			:return: zero_power_per: integer"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{cellNull_cmd_val}:ZPRS{indexNull_cmd_val}:ZPT?')
		return trim_str_response(response)
