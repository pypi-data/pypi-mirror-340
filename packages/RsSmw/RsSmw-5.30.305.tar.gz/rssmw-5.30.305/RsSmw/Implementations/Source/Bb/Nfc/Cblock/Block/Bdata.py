from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BdataCls:
	"""Bdata commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bdata", core, parent)

	def set(self, bdata: str, commandBlock=repcap.CommandBlock.Default, fmBlock=repcap.FmBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:BDATa \n
		Snippet: driver.source.bb.nfc.cblock.block.bdata.set(bdata = rawAbc, commandBlock = repcap.CommandBlock.Default, fmBlock = repcap.FmBlock.Default) \n
		Sets the value of 'Block Data' . \n
			:param bdata: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param fmBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
		"""
		param = Conversions.value_to_str(bdata)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		fmBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(fmBlock, repcap.FmBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:BLOCk{fmBlock_cmd_val}:BDATa {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default, fmBlock=repcap.FmBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:BDATa \n
		Snippet: value: str = driver.source.bb.nfc.cblock.block.bdata.get(commandBlock = repcap.CommandBlock.Default, fmBlock = repcap.FmBlock.Default) \n
		Sets the value of 'Block Data' . \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param fmBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: bdata: integer"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		fmBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(fmBlock, repcap.FmBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:BLOCk{fmBlock_cmd_val}:BDATa?')
		return trim_str_response(response)
