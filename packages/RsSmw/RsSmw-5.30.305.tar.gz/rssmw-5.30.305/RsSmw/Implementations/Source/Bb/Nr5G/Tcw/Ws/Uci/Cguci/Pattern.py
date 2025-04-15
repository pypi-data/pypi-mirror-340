from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, cgu_ci_pattern: str, cgu_ci_bit_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CGUCi:PATTern \n
		Snippet: driver.source.bb.nr5G.tcw.ws.uci.cguci.pattern.set(cgu_ci_pattern = rawAbc, cgu_ci_bit_count = 1) \n
		Defines the CG-UCI pattern. \n
			:param cgu_ci_pattern: 18 bits Bit pattern.
			:param cgu_ci_bit_count: integer Pattern length. Range: 18 to 18
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cgu_ci_pattern', cgu_ci_pattern, DataType.RawString), ArgSingle('cgu_ci_bit_count', cgu_ci_bit_count, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CGUCi:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Cgu_Ci_Pattern: str: 18 bits Bit pattern.
			- 2 Cgu_Ci_Bit_Count: int: integer Pattern length. Range: 18 to 18"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cgu_Ci_Pattern'),
			ArgStruct.scalar_int('Cgu_Ci_Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cgu_Ci_Pattern: str = None
			self.Cgu_Ci_Bit_Count: int = None

	def get(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CGUCi:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.tcw.ws.uci.cguci.pattern.get() \n
		Defines the CG-UCI pattern. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CGUCi:PATTern?', self.__class__.PatternStruct())
