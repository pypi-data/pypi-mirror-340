from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbaCls:
	"""Rba commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rba", core, parent)

	def set(self, rba: int, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default, setItem=repcap.SetItem.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:EPDCch:CELL<ST0>:SET<DIR>:RBA \n
		Snippet: driver.source.bb.v5G.downlink.user.epdcch.cell.set.rba.set(rba = 1, userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default, setItem = repcap.SetItem.Default) \n
		No command help available \n
			:param rba: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param setItem: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
		"""
		param = Conversions.decimal_value_to_str(rba)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		setItem_cmd_val = self._cmd_group.get_repcap_cmd_value(setItem, repcap.SetItem)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:EPDCch:CELL{cellNull_cmd_val}:SET{setItem_cmd_val}:RBA {param}')

	def get(self, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default, setItem=repcap.SetItem.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:EPDCch:CELL<ST0>:SET<DIR>:RBA \n
		Snippet: value: int = driver.source.bb.v5G.downlink.user.epdcch.cell.set.rba.get(userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default, setItem = repcap.SetItem.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param setItem: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: rba: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		setItem_cmd_val = self._cmd_group.get_repcap_cmd_value(setItem, repcap.SetItem)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:EPDCch:CELL{cellNull_cmd_val}:SET{setItem_cmd_val}:RBA?')
		return Conversions.str_to_int(response)
