from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sf1Cls:
	"""Sf1 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sf1", core, parent)

	def set(self, sflag_1: str, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:SF1 \n
		Snippet: driver.source.bb.nfc.cblock.sf1.set(sflag_1 = rawAbc, commandBlock = repcap.CommandBlock.Default) \n
		Sets the status flag 1 to specify a Type 3 tag's error condition. A value of 0 signals a successful execution, values
		different from 0 indicate errors. \n
			:param sflag_1: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.value_to_str(sflag_1)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:SF1 {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:SF1 \n
		Snippet: value: str = driver.source.bb.nfc.cblock.sf1.get(commandBlock = repcap.CommandBlock.Default) \n
		Sets the status flag 1 to specify a Type 3 tag's error condition. A value of 0 signals a successful execution, values
		different from 0 indicate errors. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: sflag_1: integer"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:SF1?')
		return trim_str_response(response)
