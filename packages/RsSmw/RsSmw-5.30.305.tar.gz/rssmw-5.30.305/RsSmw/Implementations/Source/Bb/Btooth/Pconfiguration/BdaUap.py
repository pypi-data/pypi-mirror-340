from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BdaUapCls:
	"""BdaUap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bdaUap", core, parent)

	def set(self, bda_uap: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:BDAUap \n
		Snippet: driver.source.bb.btooth.pconfiguration.bdaUap.set(bda_uap = rawAbc, bitcount = 1) \n
		Enters the upper address part of Bluetooth Device Address. The length of UAP is 8 bits or 2 hexadecimal figures. \n
			:param bda_uap: numeric Range: #H00 to #HFF
			:param bitcount: integer Range: 8 to 8
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bda_uap', bda_uap, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDAUap {param}'.rstrip())

	# noinspection PyTypeChecker
	class BdaUapStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Bda_Uap: str: numeric Range: #H00 to #HFF
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Bda_Uap'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bda_Uap: str = None
			self.Bitcount: int = None

	def get(self) -> BdaUapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PCONfiguration:BDAUap \n
		Snippet: value: BdaUapStruct = driver.source.bb.btooth.pconfiguration.bdaUap.get() \n
		Enters the upper address part of Bluetooth Device Address. The length of UAP is 8 bits or 2 hexadecimal figures. \n
			:return: structure: for return value, see the help for BdaUapStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDAUap?', self.__class__.BdaUapStruct())
