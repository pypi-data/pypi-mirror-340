from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IaWindowCls:
	"""IaWindow commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iaWindow", core, parent)

	def set(self, ia_window: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:IAWindow \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.iaWindow.set(ia_window = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets the parameters necessary to support an IBSS (2 bytes) . The Information field contains the ATIM Window parameter. \n
			:param ia_window: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(ia_window)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:IAWindow {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:IAWindow \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.bfConfiguration.iaWindow.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the parameters necessary to support an IBSS (2 bytes) . The Information field contains the ATIM Window parameter. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ia_window: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:IAWindow?')
		return trim_str_response(response)
