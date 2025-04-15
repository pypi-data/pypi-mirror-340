from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvParameterCls:
	"""RvParameter commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rvParameter", core, parent)

	def set(self, rv_parameter: int, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVParameter \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.rvParameter.set(rv_parameter = 1, cell = repcap.Cell.Default) \n
		(for HARQ Mode set to constant ACK) Sets the redundancy version parameter, i.e. indicates which redundancy version of the
		data is sent. \n
			:param rv_parameter: integer Range: 0 to 7
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(rv_parameter)
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:HSUPA:RVParameter {param}')

	def get(self, cell=repcap.Cell.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVParameter \n
		Snippet: value: int = driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.rvParameter.get(cell = repcap.Cell.Default) \n
		(for HARQ Mode set to constant ACK) Sets the redundancy version parameter, i.e. indicates which redundancy version of the
		data is sent. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: rv_parameter: integer Range: 0 to 7"""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:HSUPA:RVParameter?')
		return Conversions.str_to_int(response)
