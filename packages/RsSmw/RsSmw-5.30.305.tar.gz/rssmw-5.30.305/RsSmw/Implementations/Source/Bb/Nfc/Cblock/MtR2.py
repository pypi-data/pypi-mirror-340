from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MtR2Cls:
	"""MtR2 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mtR2", core, parent)

	def set(self, mt_r_2: enums.NfcMinTr2, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:MTR2 \n
		Snippet: driver.source.bb.nfc.cblock.mtR2.set(mt_r_2 = enums.NfcMinTr2.TR20, commandBlock = repcap.CommandBlock.Default) \n
		Sets the minimum value of TR2 supported. \n
			:param mt_r_2: TR20| TR21| TR22| TR23
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		param = Conversions.enum_scalar_to_str(mt_r_2, enums.NfcMinTr2)
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:MTR2 {param}')

	# noinspection PyTypeChecker
	def get(self, commandBlock=repcap.CommandBlock.Default) -> enums.NfcMinTr2:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:MTR2 \n
		Snippet: value: enums.NfcMinTr2 = driver.source.bb.nfc.cblock.mtR2.get(commandBlock = repcap.CommandBlock.Default) \n
		Sets the minimum value of TR2 supported. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: mt_r_2: TR20| TR21| TR22| TR23"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:MTR2?')
		return Conversions.str_to_scalar_enum(response, enums.NfcMinTr2)
