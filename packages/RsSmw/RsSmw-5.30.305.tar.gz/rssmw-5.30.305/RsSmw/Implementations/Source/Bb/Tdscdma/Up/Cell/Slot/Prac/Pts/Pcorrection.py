from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcorrectionCls:
	"""Pcorrection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcorrection", core, parent)

	def get(self, cell=repcap.Cell.Default, slotNull=repcap.SlotNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH0>:PRAC:PTS:PCORrection \n
		Snippet: value: float = driver.source.bb.tdscdma.up.cell.slot.prac.pts.pcorrection.get(cell = repcap.Cell.Default, slotNull = repcap.SlotNull.Default) \n
		Queries the power correction of the UpPTS.
			INTRO_CMD_HELP: The value is computed based on: \n
			- UpPTS power BB:TDSC:UP:CELL:SLOT:PRAC:PTS:POW
			- Power step BB:TDSC:UP:CELL:SLOT:PRAC:PTS:PST
			- Message power BB:TDSC:UP:CELL:SLOT:PRAC:MSG:POW
			- UpPTS length, message length BB:TDSC:UP:CELL:SLOT:PRAC:MSG:LENG
			- ARB sequence length BB:TDSC:SLEN \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:return: pcorrection: float Range: -1E10 to 1E10"""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:SLOT{slotNull_cmd_val}:PRAC:PTS:PCORrection?')
		return Conversions.str_to_float(response)
