from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuncturingCls:
	"""Puncturing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("puncturing", core, parent)

	def set(self, puncturing: bool, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:CS:PUNCturing \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.puncturing.set(puncturing = False, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Turns puncturing of the CORESET on and off.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a 5 MHz channel bandwidth ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:CBW) .
			- Select a 15 kHz subcarrier spacing ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:TXBW:S15K:USE) . \n
			:param puncturing: OFF| ON| 1| 0
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.bool_to_str(puncturing)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:PUNCturing {param}')

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:CS:PUNCturing \n
		Snippet: value: bool = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.puncturing.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Turns puncturing of the CORESET on and off.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a 5 MHz channel bandwidth ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:CBW) .
			- Select a 15 kHz subcarrier spacing ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:TXBW:S15K:USE) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: puncturing: OFF| ON| 1| 0"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:PUNCturing?')
		return Conversions.str_to_bool(response)
