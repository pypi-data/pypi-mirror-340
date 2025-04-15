from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsspbchCls:
	"""Nsspbch commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nsspbch", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:NSSPbch \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.nsspbch.get(cellNull = repcap.CellNull.Default) \n
		Sets the number of SS/PBCH patterns to be configured. For the sidelink application: number of S-SS/PSBCH patterns. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: nu_of_pbch_pattern: integer Range: 0 to 10"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:NSSPbch?')
		return Conversions.str_to_int(response)
