from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CiValueCls:
	"""CiValue commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ciValue", core, parent)

	def set(self, ci_value: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.ciValue.set(ci_value = rawAbc, bitcount = 1) \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:param ci_value: numeric
			:param bitcount: integer Range: 24 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ci_value', ci_value, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue {param}'.rstrip())

	# noinspection PyTypeChecker
	class CiValueStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ci_Value: str: numeric
			- 2 Bitcount: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Ci_Value'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ci_Value: str = None
			self.Bitcount: int = None

	def get(self) -> CiValueStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Snippet: value: CiValueStruct = driver.source.bb.btooth.econfiguration.pconfiguration.ciValue.get() \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:return: structure: for return value, see the help for CiValueStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue?', self.__class__.CiValueStruct())
