from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CivpCls:
	"""Civp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("civp", core, parent)

	def set(self, cs_iv_p: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CIVP \n
		Snippet: driver.source.bb.btooth.cs.civp.set(cs_iv_p = rawAbc, bitcount = 1) \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IV_P parameter. The parameter is 64-bit in hexadecimal
		representation. \n
			:param cs_iv_p: numeric CS_IV_P value in hexadecimal representation.
			:param bitcount: integer Fixed bit count of 64 bits. Range: 64 to 64
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cs_iv_p', cs_iv_p, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CIVP {param}'.rstrip())

	# noinspection PyTypeChecker
	class CivpStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Cs_Iv_P: str: numeric CS_IV_P value in hexadecimal representation.
			- 2 Bitcount: int: integer Fixed bit count of 64 bits. Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_Iv_P'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_Iv_P: str = None
			self.Bitcount: int = None

	def get(self) -> CivpStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CIVP \n
		Snippet: value: CivpStruct = driver.source.bb.btooth.cs.civp.get() \n
		Requires packet type CS SEQUENCE or LL_CS_SEC_REQ. Sets the CS_IV_P parameter. The parameter is 64-bit in hexadecimal
		representation. \n
			:return: structure: for return value, see the help for CivpStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CIVP?', self.__class__.CivpStruct())
