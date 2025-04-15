from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MrqCls:
	"""Mrq commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mrq", core, parent)

	def set(self, mrq: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MRQ \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.mrq.set(mrq = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		The command determines the information of the MRQ subfield. \n
			:param mrq: integer 0 requests MCS feedback (solicited MFB) . 1 otherwise
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(mrq)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MRQ {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MRQ \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.mrq.get(frameBlock = repcap.FrameBlock.Default) \n
		The command determines the information of the MRQ subfield. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: mrq: integer 0 requests MCS feedback (solicited MFB) . 1 otherwise"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MRQ?')
		return trim_str_response(response)
