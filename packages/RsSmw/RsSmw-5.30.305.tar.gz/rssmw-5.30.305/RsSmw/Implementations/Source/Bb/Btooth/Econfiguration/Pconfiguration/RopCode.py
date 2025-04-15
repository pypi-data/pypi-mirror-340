from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RopCodeCls:
	"""RopCode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ropCode", core, parent)

	def set(self, rop_code: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.ropCode.set(rop_code = rawAbc, bitcount = 1) \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:param rop_code: numeric
			:param bitcount: integer Range: 8 to 8
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('rop_code', rop_code, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode {param}'.rstrip())

	# noinspection PyTypeChecker
	class RopCodeStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Rop_Code: str: numeric
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Rop_Code'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rop_Code: str = None
			self.Bitcount: int = None

	def get(self) -> RopCodeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Snippet: value: RopCodeStruct = driver.source.bb.btooth.econfiguration.pconfiguration.ropCode.get() \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:return: structure: for return value, see the help for RopCodeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode?', self.__class__.RopCodeStruct())
