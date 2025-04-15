from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdreCls:
	"""Pdre commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdre", core, parent)

	def set(self, re_map_qcl: int, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST0>:SEQelem:PDRE \n
		Snippet: driver.source.bb.eutra.downlink.user.asPy.downlink.cell.seqElem.pdre.set(re_map_qcl = 1, userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		Sets the PDSCH RE mapping and QCL (quasi-co-location) indicator.
		See also [:SOURce<hw>]:BB:EUTRa:DL[:SUBF<st0>]:ENCC:PDCCh:EXTC:ITEM<ch0>:DCIConf:PDRE \n
			:param re_map_qcl: integer Range: 0 to 3
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(re_map_qcl)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:DL:CELL{cellNull_cmd_val}:SEQelem:PDRE {param}')

	def get(self, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST0>:SEQelem:PDRE \n
		Snippet: value: int = driver.source.bb.eutra.downlink.user.asPy.downlink.cell.seqElem.pdre.get(userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		Sets the PDSCH RE mapping and QCL (quasi-co-location) indicator.
		See also [:SOURce<hw>]:BB:EUTRa:DL[:SUBF<st0>]:ENCC:PDCCh:EXTC:ITEM<ch0>:DCIConf:PDRE \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: re_map_qcl: integer Range: 0 to 3"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:DL:CELL{cellNull_cmd_val}:SEQelem:PDRE?')
		return Conversions.str_to_int(response)
