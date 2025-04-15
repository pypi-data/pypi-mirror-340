from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CinpCls:
	"""Cinp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cinp", core, parent)

	def set(self, cs_in_p: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINP \n
		Snippet: driver.source.bb.btooth.cs.cinp.set(cs_in_p = rawAbc, bitcount = 1) \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IN_P parameter. The parameter is 32-bit in hexadecimal
		representation. \n
			:param cs_in_p: numeric CS_IN_P value in hexadecimal representation.
			:param bitcount: integer Fixed bit count of 32 bits. Range: 32 to 32
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cs_in_p', cs_in_p, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINP {param}'.rstrip())

	# noinspection PyTypeChecker
	class CinpStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Cs_In_P: str: numeric CS_IN_P value in hexadecimal representation.
			- 2 Bitcount: int: integer Fixed bit count of 32 bits. Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_In_P'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_In_P: str = None
			self.Bitcount: int = None

	def get(self) -> CinpStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINP \n
		Snippet: value: CinpStruct = driver.source.bb.btooth.cs.cinp.get() \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IN_P parameter. The parameter is 32-bit in hexadecimal
		representation. \n
			:return: structure: for return value, see the help for CinpStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CINP?', self.__class__.CinpStruct())
