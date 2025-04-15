from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DuplexingCls:
	"""Duplexing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("duplexing", core, parent)

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.OneWebDuplexModeRange:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:CA:CELL<CH0>:DUPLexing \n
		Snippet: value: enums.OneWebDuplexModeRange = driver.source.bb.oneweb.uplink.ca.cell.duplexing.get(cellNull = repcap.CellNull.Default) \n
		Queries the duplexing mode of the component carriers. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: ulca_duplex_mode: FDD"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ONEWeb:UL:CA:CELL{cellNull_cmd_val}:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.OneWebDuplexModeRange)
