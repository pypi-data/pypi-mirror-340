from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:THConfig:PID:PATTern \n
		Snippet: driver.source.bb.dvb.dvbx.thConfig.pid.pattern.set(pattern = rawAbc, bitcount = 1) \n
		Sets the packet identifier PID. \n
			:param pattern: numeric
			:param bitcount: integer Range: 13 to 13
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('pattern', pattern, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBX:THConfig:PID:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Pattern: str: numeric
			- 2 Bitcount: int: integer Range: 13 to 13"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Pattern'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: str = None
			self.Bitcount: int = None

	def get(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:THConfig:PID:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dvb.dvbx.thConfig.pid.pattern.get() \n
		Sets the packet identifier PID. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DVB:DVBX:THConfig:PID:PATTern?', self.__class__.PatternStruct())
