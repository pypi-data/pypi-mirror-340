from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdgMoreCls:
	"""RdgMore commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rdgMore", core, parent)

	def set(self, rdg_more: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:RDGMore \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.rdgMore.set(rdg_more = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the RDG/More PPDU. Transmitted by Initiator 0 = No reverse grant. 1 = A reverse grant is present, as
		defined by the Duration/ID field. Transmitted by Responder 0 = The PPDU carrying the MPDU is the last transmission by the
		responder. 1 = The PPDU carrying the frame is followed by another PPDU. \n
			:param rdg_more: integer Range: #H0,1 to #H1,1
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(rdg_more)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:RDGMore {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:RDGMore \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.htControl.rdgMore.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the RDG/More PPDU. Transmitted by Initiator 0 = No reverse grant. 1 = A reverse grant is present, as
		defined by the Duration/ID field. Transmitted by Responder 0 = The PPDU carrying the MPDU is the last transmission by the
		responder. 1 = The PPDU carrying the frame is followed by another PPDU. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: rdg_more: integer Range: #H0,1 to #H1,1"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:RDGMore?')
		return trim_str_response(response)
