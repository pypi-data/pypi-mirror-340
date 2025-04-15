from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:BLOCk:STATe \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.block.state.set(state = False, cell = repcap.Cell.Default) \n
		Activates or deactivates block error generation. \n
			:param state: 1| ON| 0| OFF
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
		"""
		param = Conversions.bool_to_str(state)
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:BLOCk:STATe {param}')

	def get(self, cell=repcap.Cell.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:BLOCk:STATe \n
		Snippet: value: bool = driver.source.bb.tdscdma.up.cell.enh.dch.block.state.get(cell = repcap.Cell.Default) \n
		Activates or deactivates block error generation. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: state: 1| ON| 0| OFF"""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:BLOCk:STATe?')
		return Conversions.str_to_bool(response)
