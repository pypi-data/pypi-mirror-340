from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DofdmCls:
	"""Dofdm commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dofdm", core, parent)

	def set(self, cd_ofdm: bool, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:DOFDm \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.dofdm.set(cd_ofdm = False, frameBlock = repcap.FrameBlock.Default) \n
		Indicates if Direct Sequence Spread Spectrum - OFDM is allowed. \n
			:param cd_ofdm: 1| ON| 0| OFF
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.bool_to_str(cd_ofdm)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:CAPability:DOFDm {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:DOFDm \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.dofdm.get(frameBlock = repcap.FrameBlock.Default) \n
		Indicates if Direct Sequence Spread Spectrum - OFDM is allowed. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: cd_ofdm: 1| ON| 0| OFF"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:CAPability:DOFDm?')
		return Conversions.str_to_bool(response)
