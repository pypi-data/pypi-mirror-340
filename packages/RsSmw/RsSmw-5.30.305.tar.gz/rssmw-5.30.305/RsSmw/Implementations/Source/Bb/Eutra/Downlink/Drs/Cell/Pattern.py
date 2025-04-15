from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, eutra_drs_pattern: List[int], cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH0>:PATTern \n
		Snippet: driver.source.bb.eutra.downlink.drs.cell.pattern.set(eutra_drs_pattern = [1, 2, 3], cellNull = repcap.CellNull.Default) \n
		Defines the subframes in that DRS is transmitted for up to 20 DRS occasions. \n
			:param eutra_drs_pattern: No help available
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.list_to_csv_str(eutra_drs_pattern)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{cellNull_cmd_val}:PATTern {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> List[int]:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH0>:PATTern \n
		Snippet: value: List[int] = driver.source.bb.eutra.downlink.drs.cell.pattern.get(cellNull = repcap.CellNull.Default) \n
		Defines the subframes in that DRS is transmitted for up to 20 DRS occasions. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: eutra_drs_pattern: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{cellNull_cmd_val}:PATTern?')
		return response
