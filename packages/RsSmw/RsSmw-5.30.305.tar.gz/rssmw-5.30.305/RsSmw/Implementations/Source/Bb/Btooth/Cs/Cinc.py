from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CincCls:
	"""Cinc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cinc", core, parent)

	def set(self, cs_in_c: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINC \n
		Snippet: driver.source.bb.btooth.cs.cinc.set(cs_in_c = rawAbc, bitcount = 1) \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IN_C parameter. The parameter is 32-bit in hexadecimal
		representation. \n
			:param cs_in_c: numeric CS_IN_C value in hexadecimal representation.
			:param bitcount: integer Fixed bit count of 32 bits. Range: 32 to 32
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cs_in_c', cs_in_c, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINC {param}'.rstrip())

	# noinspection PyTypeChecker
	class CincStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Cs_In_C: str: numeric CS_IN_C value in hexadecimal representation.
			- 2 Bitcount: int: integer Fixed bit count of 32 bits. Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_In_C'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_In_C: str = None
			self.Bitcount: int = None

	def get(self) -> CincStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINC \n
		Snippet: value: CincStruct = driver.source.bb.btooth.cs.cinc.get() \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IN_C parameter. The parameter is 32-bit in hexadecimal
		representation. \n
			:return: structure: for return value, see the help for CincStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CINC?', self.__class__.CincStruct())
