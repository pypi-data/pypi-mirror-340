from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RealCls:
	"""Real commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("real", core, parent)

	def get(self, cellNull=repcap.CellNull.Default, columnNull=repcap.ColumnNull.Default, rowNull=repcap.RowNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DUMRes:APMap:COL<APC(ST0)>:ROW<APR(DIR0)>:REAL \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.dumRes.apMap.col.row.real.get(cellNull = repcap.CellNull.Default, columnNull = repcap.ColumnNull.Default, rowNull = repcap.RowNull.Default) \n
		Define the mapping of the antenna ports to the physical antennas for unused (dummy) resource elements in cartesian
		mapping format (real value) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param columnNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: ap_real: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		columnNull_cmd_val = self._cmd_group.get_repcap_cmd_value(columnNull, repcap.ColumnNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DUMRes:APMap:COL{columnNull_cmd_val}:ROW{rowNull_cmd_val}:REAL?')
		return Conversions.str_to_float(response)
