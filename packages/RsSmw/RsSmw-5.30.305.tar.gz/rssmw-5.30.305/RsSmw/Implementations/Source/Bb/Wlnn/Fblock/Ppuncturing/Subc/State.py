from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, ppuncturing_stat: bool, frameBlock=repcap.FrameBlock.Default, subChannel=repcap.SubChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing:SUBC<DI>:STATe \n
		Snippet: driver.source.bb.wlnn.fblock.ppuncturing.subc.state.set(ppuncturing_stat = False, frameBlock = repcap.FrameBlock.Default, subChannel = repcap.SubChannel.Default) \n
		Requires enabled preamble puncturing. Selects or indicates the 20 MHz subchannel that is punctured in the preamble.
		If enabled, this subchannel is not transmitted. \n
			:param ppuncturing_stat: OFF| ON| 1| 0
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subc')
		"""
		param = Conversions.bool_to_str(ppuncturing_stat)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:PPUNcturing:SUBC{subChannel_cmd_val}:STATe {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, subChannel=repcap.SubChannel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing:SUBC<DI>:STATe \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.ppuncturing.subc.state.get(frameBlock = repcap.FrameBlock.Default, subChannel = repcap.SubChannel.Default) \n
		Requires enabled preamble puncturing. Selects or indicates the 20 MHz subchannel that is punctured in the preamble.
		If enabled, this subchannel is not transmitted. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param subChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subc')
			:return: ppuncturing_stat: OFF| ON| 1| 0"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		subChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subChannel, repcap.SubChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:PPUNcturing:SUBC{subChannel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
