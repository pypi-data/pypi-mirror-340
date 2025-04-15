from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SprSecondCls:
	"""SprSecond commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sprSecond", core, parent)

	def set(self, spatial_reuse_2: str, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default, triggerFrameUser=repcap.TriggerFrameUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST0>:SPRSecond \n
		Snippet: driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.sprSecond.set(spatial_reuse_2 = rawAbc, frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default, triggerFrameUser = repcap.TriggerFrameUser.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the following
		command: [:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param spatial_reuse_2: 3 bits
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param triggerFrameUser: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')
		"""
		param = Conversions.value_to_str(spatial_reuse_2)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		triggerFrameUser_cmd_val = self._cmd_group.get_repcap_cmd_value(triggerFrameUser, repcap.TriggerFrameUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:UINFo{triggerFrameUser_cmd_val}:SPRSecond {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default, triggerFrameUser=repcap.TriggerFrameUser.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST0>:SPRSecond \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.sprSecond.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default, triggerFrameUser = repcap.TriggerFrameUser.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the following
		command: [:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param triggerFrameUser: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')
			:return: spatial_reuse_2: No help available"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		triggerFrameUser_cmd_val = self._cmd_group.get_repcap_cmd_value(triggerFrameUser, repcap.TriggerFrameUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:UINFo{triggerFrameUser_cmd_val}:SPRSecond?')
		return trim_str_response(response)
