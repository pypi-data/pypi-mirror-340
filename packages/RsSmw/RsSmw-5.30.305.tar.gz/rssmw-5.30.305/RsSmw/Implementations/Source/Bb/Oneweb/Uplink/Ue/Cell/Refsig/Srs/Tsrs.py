from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TsrsCls:
	"""Tsrs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsrs", core, parent)

	def get(self, userEquipment=repcap.UserEquipment.Default, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS:TSRS \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.ue.cell.refsig.srs.tsrs.get(userEquipment = repcap.UserEquipment.Default, cellNull = repcap.CellNull.Default) \n
		Queries the UE-specific parameter SRS periodicity TSRS. The value depends on the selected SRS configuration index ISRS
		([:SOURce<hw>]:BB:ONEWeb:UL:UE<st>[:CELL<ccidx>]:REFSig:SRS[<srsidx>]:ISRS) and duplexing mode
		([:SOURce<hw>]:BB:ONEWeb:DUPLexing?) . \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: period_tsrs: integer Range: 0 to 65535"""
		userEquipment_cmd_val = self._cmd_group.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ONEWeb:UL:UE{userEquipment_cmd_val}:CELL{cellNull_cmd_val}:REFSig:SRS:TSRS?')
		return Conversions.str_to_int(response)
