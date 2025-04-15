from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:PATTern \n
		Snippet: driver.source.bb.wlnn.fblock.data.pattern.set(pattern = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Determines the bit pattern for the PATTern selection. The maximum length is 64 bits. \n
			:param pattern: 64 bits
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(pattern)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA:PATTern {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:PATTern \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.data.pattern.get(frameBlock = repcap.FrameBlock.Default) \n
		Determines the bit pattern for the PATTern selection. The maximum length is 64 bits. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: pattern: 64 bits"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA:PATTern?')
		return trim_str_response(response)
