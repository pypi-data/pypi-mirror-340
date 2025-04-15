from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SamplesCls:
	"""Samples commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("samples", core, parent)

	def get(self, commandBlock=repcap.CommandBlock.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:SAMPles \n
		Snippet: value: float = driver.source.bb.nfc.cblock.samples.get(commandBlock = repcap.CommandBlock.Default) \n
		Queries the total number of samples in a selected command block. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: samples: float"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:SAMPles?')
		return Conversions.str_to_float(response)
