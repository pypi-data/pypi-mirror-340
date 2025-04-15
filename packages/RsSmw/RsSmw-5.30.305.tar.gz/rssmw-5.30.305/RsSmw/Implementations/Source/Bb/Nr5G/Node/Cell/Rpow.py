from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RpowCls:
	"""Rpow commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rpow", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:RPOW \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.rpow.get(cellNull = repcap.CellNull.Default) \n
		Queries the relative power of the carrier. In the coupled mode (SCONfiguration:BASeband:SOURce CPEN) , the column is
		hidden. Offset for Carrier0 is read only and equal to 0 dB. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: carrier_rel_power: float Range: -80.0 to 10.0"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:RPOW?')
		return Conversions.str_to_float(response)
