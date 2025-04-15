from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PstartCls:
	"""Pstart commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pstart", core, parent)

	def set(self, pdsch_start: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CA:CELL<CH0>:PSTart \n
		Snippet: driver.source.bb.v5G.downlink.ca.cell.pstart.set(pdsch_start = 1, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param pdsch_start: No help available
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(pdsch_start)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:CA:CELL{cellNull_cmd_val}:PSTart {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:CA:CELL<CH0>:PSTart \n
		Snippet: value: int = driver.source.bb.v5G.downlink.ca.cell.pstart.get(cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: pdsch_start: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:CA:CELL{cellNull_cmd_val}:PSTart?')
		return Conversions.str_to_int(response)
