from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StdataCls:
	"""Stdata commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stdata", core, parent)

	def set(self, std_frame_data: str, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:STData \n
		Snippet: driver.source.bb.nfc.cblock.apGeneric.stdata.set(std_frame_data = rawAbc, commandBlock = repcap.CommandBlock.Default) \n
		Sets the data for a standard frame in hexadecimal values. \n
			:param std_frame_data: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.value_to_str(std_frame_data)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:APGeneric:STData {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:STData \n
		Snippet: value: str = driver.source.bb.nfc.cblock.apGeneric.stdata.get(commandBlock = repcap.CommandBlock.Default) \n
		Sets the data for a standard frame in hexadecimal values. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: std_frame_data: integer"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:APGeneric:STData?')
		return trim_str_response(response)
