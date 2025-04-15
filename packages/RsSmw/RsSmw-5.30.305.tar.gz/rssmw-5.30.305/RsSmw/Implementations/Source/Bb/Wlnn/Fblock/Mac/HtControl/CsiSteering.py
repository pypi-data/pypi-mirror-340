from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsiSteeringCls:
	"""CsiSteering commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csiSteering", core, parent)

	def set(self, csi_steering: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:CSISteering \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.csiSteering.set(csi_steering = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the CSI steering. 00 = CSI 01 = uncompressed Steering Matrix 10 = compressed Steering Matrix 11 =
		Reserved \n
			:param csi_steering: integer Range: #H0,2 to #H3,2
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(csi_steering)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:CSISteering {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:CSISteering \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.htControl.csiSteering.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the CSI steering. 00 = CSI 01 = uncompressed Steering Matrix 10 = compressed Steering Matrix 11 =
		Reserved \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: csi_steering: integer Range: #H0,2 to #H3,2"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:CSISteering?')
		return trim_str_response(response)
