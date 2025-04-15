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

	def set(self, state: bool, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:ILEaver:STATe \n
		Snippet: driver.source.bb.wlnn.fblock.user.ileaver.state.set(state = False, frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		The command activates/deactivates the interleaver of the data field. \n
			:param state: 0| 1| OFF| ON
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(state)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:ILEaver:STATe {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:ILEaver:STATe \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.user.ileaver.state.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		The command activates/deactivates the interleaver of the data field. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: state: 0| 1| OFF| ON"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:ILEaver:STATe?')
		return Conversions.str_to_bool(response)
