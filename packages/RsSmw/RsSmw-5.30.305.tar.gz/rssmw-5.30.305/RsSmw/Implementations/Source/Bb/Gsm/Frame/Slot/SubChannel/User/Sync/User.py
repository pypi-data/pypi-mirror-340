from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, user: str, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:SYNC:USER \n
		Snippet: driver.source.bb.gsm.frame.slot.subChannel.user.sync.user.set(user = rawAbc, frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command outputs the bit pattern of the User Sync sequence for the Access burst. The length is 64 bits. Superfluous
		bits are truncated on input. Missing bits are filled with 0. The command is valid only for selection BB:GSM:SLOT:SYNC:SEL
		USER and for burst type selection BB:GSM:SLOT:TYPE ACC. \n
			:param user: integer Range: #B0,1 to #B111...,41
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.value_to_str(user)
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SYNC:USER {param}')

	def get(self, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:SYNC:USER \n
		Snippet: value: str = driver.source.bb.gsm.frame.slot.subChannel.user.sync.user.get(frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command outputs the bit pattern of the User Sync sequence for the Access burst. The length is 64 bits. Superfluous
		bits are truncated on input. Missing bits are filled with 0. The command is valid only for selection BB:GSM:SLOT:SYNC:SEL
		USER and for burst type selection BB:GSM:SLOT:TYPE ACC. \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: user: integer Range: #B0,1 to #B111...,41"""
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SYNC:USER?')
		return trim_str_response(response)
