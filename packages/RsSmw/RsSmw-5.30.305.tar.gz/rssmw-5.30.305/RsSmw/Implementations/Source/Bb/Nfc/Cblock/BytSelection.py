from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BytSelectionCls:
	"""BytSelection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bytSelection", core, parent)

	def set(self, byte_sel: int, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BYTSelection \n
		Snippet: driver.source.bb.nfc.cblock.bytSelection.set(byte_sel = 1, commandBlock = repcap.CommandBlock.Default) \n
		Selects a byte to be read/written. \n
			:param byte_sel: integer Range: 0 to 7
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.decimal_value_to_str(byte_sel)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:BYTSelection {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BYTSelection \n
		Snippet: value: int = driver.source.bb.nfc.cblock.bytSelection.get(commandBlock = repcap.CommandBlock.Default) \n
		Selects a byte to be read/written. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: byte_sel: integer Range: 0 to 7"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:BYTSelection?')
		return Conversions.str_to_int(response)
