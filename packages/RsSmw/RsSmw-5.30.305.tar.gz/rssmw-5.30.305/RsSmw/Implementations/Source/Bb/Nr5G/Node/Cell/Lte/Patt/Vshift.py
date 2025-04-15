from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VshiftCls:
	"""Vshift commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vshift", core, parent)

	def get(self, cellNull=repcap.CellNull.Default, patternNull=repcap.PatternNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:LTE:PATT<ST0>:VSHift \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.lte.patt.vshift.get(cellNull = repcap.CellNull.Default, patternNull = repcap.PatternNull.Default) \n
		Selects the vShift parameter for an LTE signal.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on LTE-CRS coexistence ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:LTE:STATe) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param patternNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Patt')
			:return: lte_vshift: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		patternNull_cmd_val = self._cmd_group.get_repcap_cmd_value(patternNull, repcap.PatternNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:LTE:PATT{patternNull_cmd_val}:VSHift?')
		return Conversions.str_to_int(response)
