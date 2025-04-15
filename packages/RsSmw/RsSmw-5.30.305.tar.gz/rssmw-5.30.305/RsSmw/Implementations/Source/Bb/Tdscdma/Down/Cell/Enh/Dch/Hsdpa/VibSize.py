from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VibSizeCls:
	"""VibSize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vibSize", core, parent)

	def set(self, vib_size: int, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:VIBSize \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.hsdpa.vibSize.set(vib_size = 1, cell = repcap.Cell.Default) \n
		Sets the size of the virtual IR buffer. \n
			:param vib_size: integer Range: dynamic to 63360
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(vib_size)
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:HSDPA:VIBSize {param}')

	def get(self, cell=repcap.Cell.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:VIBSize \n
		Snippet: value: int = driver.source.bb.tdscdma.down.cell.enh.dch.hsdpa.vibSize.get(cell = repcap.Cell.Default) \n
		Sets the size of the virtual IR buffer. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: vib_size: integer Range: dynamic to 63360"""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:HSDPA:VIBSize?')
		return Conversions.str_to_int(response)
