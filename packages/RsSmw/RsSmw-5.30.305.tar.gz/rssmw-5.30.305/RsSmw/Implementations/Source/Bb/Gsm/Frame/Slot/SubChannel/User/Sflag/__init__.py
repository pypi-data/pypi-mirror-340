from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SflagCls:
	"""Sflag commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sflag", core, parent)

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Use import UseCls
			self._use = UseCls(self._core, self._cmd_group)
		return self._use

	def set(self, sflag: str, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:SFLag \n
		Snippet: driver.source.bb.gsm.frame.slot.subChannel.user.sflag.set(sflag = rawAbc, frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command sets the Stealing Flag state (only for Normal burst BB:GSM:SLOT:TYPE NORM) . \n
			:param sflag: 0| 1
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.value_to_str(sflag)
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SFLag {param}')

	def get(self, frameIx=repcap.FrameIx.Default, slotNull=repcap.SlotNull.Default, subChannel=repcap.SubChannel.Default, userIx=repcap.UserIx.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST0>:[SUBChannel<US>]:[USER<CH>]:SFLag \n
		Snippet: value: str = driver.source.bb.gsm.frame.slot.subChannel.user.sflag.get(frameIx = repcap.FrameIx.Default, slotNull = repcap.SlotNull.Default, subChannel = repcap.SubChannel.Default, userIx = repcap.UserIx.Default) \n
		The command sets the Stealing Flag state (only for Normal burst BB:GSM:SLOT:TYPE NORM) . \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param slotNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Slot')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: sflag: 0| 1"""
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		slotNull_cmd_val = self._cmd_group.get_repcap_cmd_value(slotNull, repcap.SlotNull)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{slotNull_cmd_val}:SUBChannel{subChannel_cmd_val}:USER{userIx_cmd_val}:SFLag?')
		return trim_str_response(response)

	def clone(self) -> 'SflagCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SflagCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
