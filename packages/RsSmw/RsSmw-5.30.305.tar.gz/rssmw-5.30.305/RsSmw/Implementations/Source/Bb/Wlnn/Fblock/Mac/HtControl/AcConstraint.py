from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcConstraintCls:
	"""AcConstraint commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acConstraint", core, parent)

	def set(self, ac_constraint: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ACConstraint \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.acConstraint.set(ac_constraint = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the AC signal field. 0 = The response may contain data from any TID (Traffic Identifier) . 1 = The
		response may contain data only from the same AC as the last Data received from the initiator. \n
			:param ac_constraint: integer Range: #H0,1 to #H1,1
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(ac_constraint)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:ACConstraint {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ACConstraint \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.htControl.acConstraint.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the AC signal field. 0 = The response may contain data from any TID (Traffic Identifier) . 1 = The
		response may contain data only from the same AC as the last Data received from the initiator. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ac_constraint: integer Range: #H0,1 to #H1,1"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:ACConstraint?')
		return trim_str_response(response)
