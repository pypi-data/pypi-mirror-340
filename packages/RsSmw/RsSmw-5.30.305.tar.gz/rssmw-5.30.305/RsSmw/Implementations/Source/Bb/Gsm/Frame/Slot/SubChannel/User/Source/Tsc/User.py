from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.Utilities import trim_str_response
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, user: str, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:[SOURce]:TSC:USER \n
		Snippet: driver.source.bb.gsm.frame.slot.subChannel.user.source.tsc.user.set(user = rawAbc, frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command specifies the user-defined training sequence code. This code is used if the USER parameter is set with the
		aid of the [:SOURce<hw>]:BB:GSM[:FRAMe<di>]:SLOT<st0>[:SUBChannel<us>][:USER<ch>][:SOURce]:TSC:SELect command. The length
		is 26 bits for BB:GSM:SLOT:TYPE NORMal and 78 bits for BB:GSM:SLOT:TYPE EDGE. \n
			:param user: integer Range: #B0,1 to #B111 ,1...26/78 bits
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
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SOURce:TSC:USER {param}')

	def get(self, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:[SOURce]:TSC:USER \n
		Snippet: value: str = driver.source.bb.gsm.frame.slot.subChannel.user.source.tsc.user.get(frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command specifies the user-defined training sequence code. This code is used if the USER parameter is set with the
		aid of the [:SOURce<hw>]:BB:GSM[:FRAMe<di>]:SLOT<st0>[:SUBChannel<us>][:USER<ch>][:SOURce]:TSC:SELect command. The length
		is 26 bits for BB:GSM:SLOT:TYPE NORMal and 78 bits for BB:GSM:SLOT:TYPE EDGE. \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: user: integer Range: #B0,1 to #B111 ,1...26/78 bits"""
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SOURce:TSC:USER?')
		return trim_str_response(response)
