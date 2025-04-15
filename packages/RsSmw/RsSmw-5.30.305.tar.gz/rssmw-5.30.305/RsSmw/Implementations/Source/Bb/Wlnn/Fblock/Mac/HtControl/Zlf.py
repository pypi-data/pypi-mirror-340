from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZlfCls:
	"""Zlf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zlf", core, parent)

	def set(self, zlf: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ZLF \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.zlf.set(zlf = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the ZLF announcement. 0 = no ZLF will follow 1 = ZLF will follow \n
			:param zlf: integer Range: #H0,1 to #H1,1
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(zlf)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:ZLF {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ZLF \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.htControl.zlf.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the ZLF announcement. 0 = no ZLF will follow 1 = ZLF will follow \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: zlf: integer Range: #H0,1 to #H1,1"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:ZLF?')
		return trim_str_response(response)
