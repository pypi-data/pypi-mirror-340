from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScIndexCls:
	"""ScIndex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scIndex", core, parent)

	def set(self, sched_cell_index: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:SCINdex \n
		Snippet: driver.source.bb.eutra.downlink.ca.cell.scIndex.set(sched_cell_index = 1, cellNull = repcap.CellNull.Default) \n
		Defines the component carrier/cell that signals the UL and DL grants for the selected SCell. \n
			:param sched_cell_index: integer Range: 0 to 7
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(sched_cell_index)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:SCINdex {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:SCINdex \n
		Snippet: value: int = driver.source.bb.eutra.downlink.ca.cell.scIndex.get(cellNull = repcap.CellNull.Default) \n
		Defines the component carrier/cell that signals the UL and DL grants for the selected SCell. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: sched_cell_index: integer Range: 0 to 7"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:SCINdex?')
		return Conversions.str_to_int(response)
