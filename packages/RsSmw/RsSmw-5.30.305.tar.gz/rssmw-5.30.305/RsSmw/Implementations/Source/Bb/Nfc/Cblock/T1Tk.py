from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class T1TkCls:
	"""T1Tk commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("t1Tk", core, parent)

	def set(self, t_1_totk: str, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:T1TK \n
		Snippet: driver.source.bb.nfc.cblock.t1Tk.set(t_1_totk = rawAbc, commandBlock = repcap.CommandBlock.Default) \n
		For number of historical bytes k greater than 0: sets the historical bytes T1 to Tk. \n
			:param t_1_totk: integer
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.value_to_str(t_1_totk)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:T1TK {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:T1TK \n
		Snippet: value: str = driver.source.bb.nfc.cblock.t1Tk.get(commandBlock = repcap.CommandBlock.Default) \n
		For number of historical bytes k greater than 0: sets the historical bytes T1 to Tk. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: t_1_totk: integer"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:T1TK?')
		return trim_str_response(response)
