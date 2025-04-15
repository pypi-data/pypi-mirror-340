from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EcodeCls:
	"""Ecode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ecode", core, parent)

	def set(self, ecode: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ECODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.ecode.set(ecode = rawAbc, bitcount = 1) \n
		Sets an 8-bit error code. For an LL_CS_TERMINATE_IND packet, informs the remote device about the termination of the
		connection. \n
			:param ecode: numeric
			:param bitcount: integer Range: 8 to 8
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ecode', ecode, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ECODe {param}'.rstrip())

	# noinspection PyTypeChecker
	class EcodeStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ecode: str: numeric
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Ecode'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ecode: str = None
			self.Bitcount: int = None

	def get(self) -> EcodeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ECODe \n
		Snippet: value: EcodeStruct = driver.source.bb.btooth.cs.cdata.ecode.get() \n
		Sets an 8-bit error code. For an LL_CS_TERMINATE_IND packet, informs the remote device about the termination of the
		connection. \n
			:return: structure: for return value, see the help for EcodeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ECODe?', self.__class__.EcodeStruct())
