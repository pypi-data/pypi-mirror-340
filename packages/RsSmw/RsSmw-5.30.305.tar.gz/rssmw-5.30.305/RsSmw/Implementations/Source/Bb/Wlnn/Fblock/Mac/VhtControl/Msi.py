from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsiCls:
	"""Msi commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msi", core, parent)

	def set(self, msi: str, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MSI \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.msi.set(msi = rawAbc, frameBlock = repcap.FrameBlock.Default) \n
		The command sets the MSI subfield. MRQ = 0 When the MRQ subfield is set to 0, the MSI subfield is reserved. MRQ = 1 When
		the MRQ subfield is set to 1, the MSI subfield contains a sequence number in the range 0 to 6 that identifies the
		specific request. \n
			:param msi: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.value_to_str(msi)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MSI {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MSI \n
		Snippet: value: str = driver.source.bb.wlnn.fblock.mac.vhtControl.msi.get(frameBlock = repcap.FrameBlock.Default) \n
		The command sets the MSI subfield. MRQ = 0 When the MRQ subfield is set to 0, the MSI subfield is reserved. MRQ = 1 When
		the MRQ subfield is set to 1, the MSI subfield contains a sequence number in the range 0 to 6 that identifies the
		specific request. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: msi: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:MSI?')
		return trim_str_response(response)
