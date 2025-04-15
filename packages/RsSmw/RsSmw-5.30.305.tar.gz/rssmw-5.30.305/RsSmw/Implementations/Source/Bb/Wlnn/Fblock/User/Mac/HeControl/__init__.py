from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HeControlCls:
	"""HeControl commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("heControl", core, parent)

	@property
	def acontrol(self):
		"""acontrol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acontrol'):
			from .Acontrol import AcontrolCls
			self._acontrol = AcontrolCls(self._core, self._cmd_group)
		return self._acontrol

	@property
	def heIndicator(self):
		"""heIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_heIndicator'):
			from .HeIndicator import HeIndicatorCls
			self._heIndicator = HeIndicatorCls(self._core, self._cmd_group)
		return self._heIndicator

	def set(self, he_control: str, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl \n
		Snippet: driver.source.bb.wlnn.fblock.user.mac.heControl.set(he_control = rawAbc, frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Sets the value with the length of 4 bytes of the HE control field. \n
			:param he_control: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.value_to_str(he_control)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:MAC:HEControl {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.user.mac.heControl.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Sets the value with the length of 4 bytes of the HE control field. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: he_control: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:MAC:HEControl?')
		return trim_str_response(response)

	def clone(self) -> 'HeControlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HeControlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
