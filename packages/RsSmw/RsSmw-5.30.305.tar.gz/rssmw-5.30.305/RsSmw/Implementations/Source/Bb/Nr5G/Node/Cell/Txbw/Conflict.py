from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConflictCls:
	"""Conflict commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("conflict", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TXBW:CONFlict \n
		Snippet: value: bool = driver.source.bb.nr5G.node.cell.txbw.conflict.get(cellNull = repcap.CellNull.Default) \n
		Queries whether there is a conflict. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: conflict: 1| ON| 0| OFF"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TXBW:CONFlict?')
		return Conversions.str_to_bool(response)
