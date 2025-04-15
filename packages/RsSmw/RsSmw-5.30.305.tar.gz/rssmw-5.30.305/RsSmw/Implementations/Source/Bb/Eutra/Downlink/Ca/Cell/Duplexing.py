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

	def set(self, dl_duplexmode: enums.EutraDuplexModeExtRange, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:DUPLexing \n
		Snippet: driver.source.bb.eutra.downlink.ca.cell.duplexing.set(dl_duplexmode = enums.EutraDuplexModeExtRange.FDD, cellNull = repcap.CellNull.Default) \n
		Selects the duplexing mode of the component carriers. \n
			:param dl_duplexmode: TDD| FDD | LAA
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(dl_duplexmode, enums.EutraDuplexModeExtRange)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.EutraDuplexModeExtRange:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH0>:DUPLexing \n
		Snippet: value: enums.EutraDuplexModeExtRange = driver.source.bb.eutra.downlink.ca.cell.duplexing.get(cellNull = repcap.CellNull.Default) \n
		Selects the duplexing mode of the component carriers. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: dl_duplexmode: TDD| FDD | LAA"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{cellNull_cmd_val}:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexModeExtRange)
