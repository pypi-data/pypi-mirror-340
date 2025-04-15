from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlIndexCls:
	"""UlIndex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ulIndex", core, parent)

	def set(self, ul_index: int, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST0>:SEQelem:ULINdex \n
		Snippet: driver.source.bb.eutra.downlink.user.asPy.uplink.cell.seqElem.ulIndex.set(ul_index = 1, userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		In TDD mode and with 'UL/DL Configuration = 0', sets the parameter UL Index. \n
			:param ul_index: integer Range: 0 to 3
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(ul_index)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:UL:CELL{cellNull_cmd_val}:SEQelem:ULINdex {param}')

	def get(self, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST0>:SEQelem:ULINdex \n
		Snippet: value: int = driver.source.bb.eutra.downlink.user.asPy.uplink.cell.seqElem.ulIndex.get(userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		In TDD mode and with 'UL/DL Configuration = 0', sets the parameter UL Index. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: ul_index: integer Range: 0 to 3"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:UL:CELL{cellNull_cmd_val}:SEQelem:ULINdex?')
		return Conversions.str_to_int(response)
