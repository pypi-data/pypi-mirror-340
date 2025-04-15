from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtOffsetCls:
	"""CtOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctOffset", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:CTOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.tmph.ctOffset.get(cellNull = repcap.CellNull.Default) \n
		Defines a cell specific custom timing advance offset in terms of time (Tc) .
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select more than one carrier ([:SOURce<hw>]:BB:NR5G:NODE:NCARrier) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: cust_timing_offs: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:CTOFfset?')
		return Conversions.str_to_int(response)
