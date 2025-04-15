from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReservedCls:
	"""Reserved commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reserved", core, parent)

	def set(self, reserved: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:REServed \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.reserved.set(reserved = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		This signal field is currently defined, but not used. It is set to zero by the transmitter and ignored by the receiver. \n
			:param reserved: integer Range: #H0,5 to #H5,2
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(reserved)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:REServed {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:REServed \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.htControl.reserved.get(frameBlock = repcap.FrameBlock.Default) \n
		This signal field is currently defined, but not used. It is set to zero by the transmitter and ignored by the receiver. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: reserved: integer Range: #H0,5 to #H5,2"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:REServed?')
		return trim_str_response(response)
