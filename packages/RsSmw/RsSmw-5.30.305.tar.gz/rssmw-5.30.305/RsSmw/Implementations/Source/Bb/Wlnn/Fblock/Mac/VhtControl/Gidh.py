from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GidhCls:
	"""Gidh commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gidh", core, parent)

	def set(self, gidh: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:GIDH \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.gidh.set(gidh = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		Sets GID-H subfield. If the Unsolicited MFB subfield is set to 1, the GID-H subfield contains the highest 3 bits of Group
		ID of the PPDU to which the unsolicited MFB refers. Otherwise this subfield is reserved. \n
			:param gidh: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(gidh)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:GIDH {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:GIDH \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.gidh.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets GID-H subfield. If the Unsolicited MFB subfield is set to 1, the GID-H subfield contains the highest 3 bits of Group
		ID of the PPDU to which the unsolicited MFB refers. Otherwise this subfield is reserved. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: gidh: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:GIDH?')
		return trim_str_response(response)
