from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nid2Cls:
	"""Nid2 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nid2", core, parent)

	def set(self, nfcid_2: str, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NID2 \n
		Snippet: driver.source.bb.nfc.cblock.nid2.set(nfcid_2 = rawAbc, commandBlock = repcap.CommandBlock.Default) \n
		Determines the entire value of NFCID2. Is a virtual parameter for SCPI to set the NFCID2 either in NFC-DEP or Type 3 Tag
		mode. \n
			:param nfcid_2: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.value_to_str(nfcid_2)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:NID2 {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NID2 \n
		Snippet: value: str = driver.source.bb.nfc.cblock.nid2.get(commandBlock = repcap.CommandBlock.Default) \n
		Determines the entire value of NFCID2. Is a virtual parameter for SCPI to set the NFCID2 either in NFC-DEP or Type 3 Tag
		mode. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nfcid_2: integer"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:NID2?')
		return trim_str_response(response)
