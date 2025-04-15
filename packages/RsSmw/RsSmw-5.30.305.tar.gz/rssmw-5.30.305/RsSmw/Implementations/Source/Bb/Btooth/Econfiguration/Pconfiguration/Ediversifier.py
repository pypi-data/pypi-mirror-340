from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EdiversifierCls:
	"""Ediversifier commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ediversifier", core, parent)

	def set(self, ediversifier: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.ediversifier.set(ediversifier = rawAbc, bitcount = 1) \n
		Sets the encrypted diversifier of the Central for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:param ediversifier: numeric
			:param bitcount: integer Range: 16 to 16
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ediversifier', ediversifier, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier {param}'.rstrip())

	# noinspection PyTypeChecker
	class EdiversifierStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ediversifier: str: numeric
			- 2 Bitcount: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Ediversifier'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ediversifier: str = None
			self.Bitcount: int = None

	def get(self) -> EdiversifierStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Snippet: value: EdiversifierStruct = driver.source.bb.btooth.econfiguration.pconfiguration.ediversifier.get() \n
		Sets the encrypted diversifier of the Central for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:return: structure: for return value, see the help for EdiversifierStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier?', self.__class__.EdiversifierStruct())
