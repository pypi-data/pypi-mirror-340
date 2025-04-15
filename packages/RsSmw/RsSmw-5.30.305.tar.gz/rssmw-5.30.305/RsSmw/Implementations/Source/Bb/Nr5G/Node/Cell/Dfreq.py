from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DfreqCls:
	"""Dfreq commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dfreq", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DFReq \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.dfreq.get(cellNull = repcap.CellNull.Default) \n
		Shifts the signal relative to the center output frequency. Use different frequency offsets to separate the channels of
		the configured and enabled cells. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: delta_fto_dc: float Range: -40E6 to 40E6"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DFReq?')
		return Conversions.str_to_float(response)
