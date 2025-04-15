from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QosCls:
	"""Qos commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qos", core, parent)

	def set(self, qos: bool, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:QOS \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.qos.set(qos = False, frameBlock = repcap.FrameBlock.Default) \n
		Informs the associated stations if quality of service (QoS) is supported. \n
			:param qos: 1| ON| 0| OFF
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.bool_to_str(qos)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:CAPability:QOS {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:QOS \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.qos.get(frameBlock = repcap.FrameBlock.Default) \n
		Informs the associated stations if quality of service (QoS) is supported. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: qos: 1| ON| 0| OFF"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BFConfiguration:CAPability:QOS?')
		return Conversions.str_to_bool(response)
