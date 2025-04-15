from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PpuncturingCls:
	"""Ppuncturing commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ppuncturing", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def subc(self):
		"""subc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_subc'):
			from .Subc import SubcCls
			self._subc = SubcCls(self._core, self._cmd_group)
		return self._subc

	def set(self, preamble_punc_bw: enums.WlannFbPpduPreamblePuncturingBw, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing \n
		Snippet: driver.source.bb.wlnn.fblock.ppuncturing.set(preamble_punc_bw = enums.WlannFbPpduPreamblePuncturingBw.BW4, frameBlock = repcap.FrameBlock.Default) \n
		Sets the bandwidth mode of preamble puncturing. \n
			:param preamble_punc_bw: BW4| BW5| BW6| BW7 BW4|BW5 Sets the bandwidth mode for HE80 channels. BW6|BW7 Sets the bandwidth mode for HE8080 channels.
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.enum_scalar_to_str(preamble_punc_bw, enums.WlannFbPpduPreamblePuncturingBw)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:PPUNcturing {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default) -> enums.WlannFbPpduPreamblePuncturingBw:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing \n
		Snippet: value: enums.WlannFbPpduPreamblePuncturingBw = driver.source.bb.wlnn.fblock.ppuncturing.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the bandwidth mode of preamble puncturing. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: preamble_punc_bw: BW4| BW5| BW6| BW7 BW4|BW5 Sets the bandwidth mode for HE80 channels. BW6|BW7 Sets the bandwidth mode for HE8080 channels."""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:PPUNcturing?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduPreamblePuncturingBw)

	def clone(self) -> 'PpuncturingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PpuncturingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
