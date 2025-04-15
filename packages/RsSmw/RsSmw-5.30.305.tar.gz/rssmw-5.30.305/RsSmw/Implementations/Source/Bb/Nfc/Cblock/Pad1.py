from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pad1Cls:
	"""Pad1 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pad1", core, parent)

	def set(self, pad_1: str, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:PAD1 \n
		Snippet: driver.source.bb.nfc.cblock.pad1.set(pad_1 = rawAbc, commandBlock = repcap.CommandBlock.Default) \n
		Sets the value of PAD0/PAD1/PAD2 (hex) . \n
			:param pad_1: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.value_to_str(pad_1)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:PAD1 {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:PAD1 \n
		Snippet: value: str = driver.source.bb.nfc.cblock.pad1.get(commandBlock = repcap.CommandBlock.Default) \n
		Sets the value of PAD0/PAD1/PAD2 (hex) . \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: pad_1: No help available"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:PAD1?')
		return trim_str_response(response)
