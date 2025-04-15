from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MfbCls:
	"""Mfb commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mfb", core, parent)

	def set(self, mfb: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MFB \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.mfb.set(mfb = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		The command sets the MFB subfield. This subfield contains the recommended MFB. The value of MCS=15 and VHT N_STS=7
		indicates that no feedback is present. See also Table 'MFB subfield in the VHT format HT control field' for definition of
		the MFB subfield. \n
			:param mfb: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(mfb)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MFB {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MFB \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.mfb.get(frameBlock = repcap.FrameBlock.Default) \n
		The command sets the MFB subfield. This subfield contains the recommended MFB. The value of MCS=15 and VHT N_STS=7
		indicates that no feedback is present. See also Table 'MFB subfield in the VHT format HT control field' for definition of
		the MFB subfield. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: mfb: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MFB?')
		return trim_str_response(response)
