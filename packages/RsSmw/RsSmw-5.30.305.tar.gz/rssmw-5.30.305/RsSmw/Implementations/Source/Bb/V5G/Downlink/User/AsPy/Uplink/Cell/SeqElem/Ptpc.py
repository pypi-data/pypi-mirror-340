from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtpcCls:
	"""Ptpc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptpc", core, parent)

	def set(self, pusch_tpc: int, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:UL:CELL<ST0>:SEQelem:PTPC \n
		Snippet: driver.source.bb.v5G.downlink.user.asPy.uplink.cell.seqElem.ptpc.set(pusch_tpc = 1, userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param pusch_tpc: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(pusch_tpc)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:UL:CELL{cellNull_cmd_val}:SEQelem:PTPC {param}')

	def get(self, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:UL:CELL<ST0>:SEQelem:PTPC \n
		Snippet: value: int = driver.source.bb.v5G.downlink.user.asPy.uplink.cell.seqElem.ptpc.get(userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: pusch_tpc: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:UL:CELL{cellNull_cmd_val}:SEQelem:PTPC?')
		return Conversions.str_to_int(response)
