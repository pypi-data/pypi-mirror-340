from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmrsCls:
	"""Dmrs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmrs", core, parent)

	def set(self, ulca_n_1_dmrs: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:CA:CELL<CH0>:DMRS \n
		Snippet: driver.source.bb.oneweb.uplink.ca.cell.dmrs.set(ulca_n_1_dmrs = 1, cellNull = repcap.CellNull.Default) \n
		Sets the parameter n(1) _DMRS per component carrier. \n
			:param ulca_n_1_dmrs: integer Range: 0 to 11
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(ulca_n_1_dmrs)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:CA:CELL{cellNull_cmd_val}:DMRS {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:CA:CELL<CH0>:DMRS \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.ca.cell.dmrs.get(cellNull = repcap.CellNull.Default) \n
		Sets the parameter n(1) _DMRS per component carrier. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: ulca_n_1_dmrs: integer Range: 0 to 11"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ONEWeb:UL:CA:CELL{cellNull_cmd_val}:DMRS?')
		return Conversions.str_to_int(response)
