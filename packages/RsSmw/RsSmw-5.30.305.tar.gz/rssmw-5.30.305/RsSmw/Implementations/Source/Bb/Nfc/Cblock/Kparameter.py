from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class KparameterCls:
	"""Kparameter commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("kparameter", core, parent)

	def set(self, kparameter: int, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:KPARameter \n
		Snippet: driver.source.bb.nfc.cblock.kparameter.set(kparameter = 1, commandBlock = repcap.CommandBlock.Default) \n
		Determines the number of historical bytes (T1 to Tk) . \n
			:param kparameter: integer Range: 0 to 15
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.decimal_value_to_str(kparameter)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:KPARameter {param}')

	def get(self, commandBlock=repcap.CommandBlock.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:KPARameter \n
		Snippet: value: int = driver.source.bb.nfc.cblock.kparameter.get(commandBlock = repcap.CommandBlock.Default) \n
		Determines the number of historical bytes (T1 to Tk) . \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: kparameter: integer Range: 0 to 15"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:KPARameter?')
		return Conversions.str_to_int(response)
