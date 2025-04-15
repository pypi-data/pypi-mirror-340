from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FcontrolCls:
	"""Fcontrol commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fcontrol", core, parent)

	def set(self, fcontrol: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:FCONtrol:FCONtrol \n
		Snippet: driver.source.bb.wlnn.fblock.mac.fcontrol.fcontrol.set(fcontrol = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		No command help available \n
			:param fcontrol: No help available
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(fcontrol)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:FCONtrol:FCONtrol {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:FCONtrol:FCONtrol \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.fcontrol.fcontrol.get(frameBlock = repcap.FrameBlock.Default) \n
		No command help available \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: fcontrol: No help available"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:FCONtrol:FCONtrol?')
		return trim_str_response(response)
