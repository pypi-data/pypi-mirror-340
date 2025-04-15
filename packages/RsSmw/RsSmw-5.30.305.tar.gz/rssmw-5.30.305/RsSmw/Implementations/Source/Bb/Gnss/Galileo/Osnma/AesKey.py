from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AesKeyCls:
	"""AesKey commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aesKey", core, parent)

	# noinspection PyTypeChecker
	def get_length(self) -> enums.OsnmaAes:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:AESKey:LENGth \n
		Snippet: value: enums.OsnmaAes = driver.source.bb.gnss.galileo.osnma.aesKey.get_length() \n
		Sets the length of the cipher-based message authentication code (CMAC) key. Setting requires a MAC Function (MF) field
		value of 1: SOURce1:BB:GNSS:GALileo:OSNMa:MF 1 See also [:SOURce<hw>]:BB:GNSS:GALileo:OSNMa:MF. \n
			:return: key_length: AES128| AES256 AES128 The length of the CMAC key is 128 bits. AES256 The length of the CMAC key is 256 bits.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:AESKey:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaAes)

	def set_length(self, key_length: enums.OsnmaAes) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:AESKey:LENGth \n
		Snippet: driver.source.bb.gnss.galileo.osnma.aesKey.set_length(key_length = enums.OsnmaAes.AES128) \n
		Sets the length of the cipher-based message authentication code (CMAC) key. Setting requires a MAC Function (MF) field
		value of 1: SOURce1:BB:GNSS:GALileo:OSNMa:MF 1 See also [:SOURce<hw>]:BB:GNSS:GALileo:OSNMa:MF. \n
			:param key_length: AES128| AES256 AES128 The length of the CMAC key is 128 bits. AES256 The length of the CMAC key is 256 bits.
		"""
		param = Conversions.enum_scalar_to_str(key_length, enums.OsnmaAes)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:AESKey:LENGth {param}')
