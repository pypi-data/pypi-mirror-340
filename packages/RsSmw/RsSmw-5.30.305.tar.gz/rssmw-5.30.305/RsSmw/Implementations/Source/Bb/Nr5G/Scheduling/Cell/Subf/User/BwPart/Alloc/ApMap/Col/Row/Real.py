from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RealCls:
	"""Real commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("real", core, parent)

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, columnNull=repcap.ColumnNull.Default, rowNull=repcap.RowNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:APMap:COL<APC(S2US0)>:ROW<APR(S3US0)>:REAL \n
		Snippet: value: float = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.real.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, columnNull = repcap.ColumnNull.Default, rowNull = repcap.RowNull.Default) \n
		Define the mapping of the antenna ports to the physical antennas. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param columnNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: ap_map_data_real: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		columnNull_cmd_val = self._cmd_group.get_repcap_cmd_value(columnNull, repcap.ColumnNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:APMap:COL{columnNull_cmd_val}:ROW{rowNull_cmd_val}:REAL?')
		return Conversions.str_to_float(response)
