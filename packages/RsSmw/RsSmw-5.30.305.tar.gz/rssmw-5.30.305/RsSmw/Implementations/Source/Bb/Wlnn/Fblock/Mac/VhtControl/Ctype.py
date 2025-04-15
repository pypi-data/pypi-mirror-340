from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtypeCls:
	"""Ctype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctype", core, parent)

	def set(self, ctype: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:CTYPe \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.ctype.set(ctype = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		The command sets the coding information. If the Unsolicited MFB subfield is set to 1, the Coding Type subfield contains
		the Coding information (set to 0 for BCC and set to 1 for LDPC) to which the unsolicited MFB refers. \n
			:param ctype: integer 0 BCC 1 LDPC
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(ctype)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:CTYPe {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:CTYPe \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.ctype.get(frameBlock = repcap.FrameBlock.Default) \n
		The command sets the coding information. If the Unsolicited MFB subfield is set to 1, the Coding Type subfield contains
		the Coding information (set to 0 for BCC and set to 1 for LDPC) to which the unsolicited MFB refers. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ctype: integer 0 BCC 1 LDPC"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:CTYPe?')
		return trim_str_response(response)
