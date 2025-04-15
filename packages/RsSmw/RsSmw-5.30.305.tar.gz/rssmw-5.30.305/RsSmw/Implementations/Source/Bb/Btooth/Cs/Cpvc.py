from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpvcCls:
	"""Cpvc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cpvc", core, parent)

	def set(self, cs_pv_c: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CPVC \n
		Snippet: driver.source.bb.btooth.cs.cpvc.set(cs_pv_c = rawAbc, bitcount = 1) \n
		No command help available \n
			:param cs_pv_c: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cs_pv_c', cs_pv_c, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CPVC {param}'.rstrip())

	# noinspection PyTypeChecker
	class CpvcStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Cs_Pv_C: str: No parameter help available
			- 2 Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_Pv_C'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_Pv_C: str = None
			self.Bitcount: int = None

	def get(self) -> CpvcStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CPVC \n
		Snippet: value: CpvcStruct = driver.source.bb.btooth.cs.cpvc.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CpvcStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CPVC?', self.__class__.CpvcStruct())
