from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AaddressCls:
	"""Aaddress commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aaddress", core, parent)

	def set(self, aaddress: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.aaddress.set(aaddress = rawAbc, bitcount = 1) \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:param aaddress: numeric
			:param bitcount: integer Range: 32 to 32
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('aaddress', aaddress, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress {param}'.rstrip())

	# noinspection PyTypeChecker
	class AaddressStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Aaddress: str: numeric
			- 2 Bitcount: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Aaddress'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aaddress: str = None
			self.Bitcount: int = None

	def get(self) -> AaddressStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Snippet: value: AaddressStruct = driver.source.bb.btooth.econfiguration.pconfiguration.aaddress.get() \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:return: structure: for return value, see the help for AaddressStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress?', self.__class__.AaddressStruct())
