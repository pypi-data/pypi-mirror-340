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

	def set(self, sync: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:BHConfig:SBYTe:PATTern \n
		Snippet: driver.source.bb.dvb.dvbx.bhConfig.sbyte.pattern.set(sync = rawAbc, bitcount = 1) \n
		Sets the user packet synchronization byte. \n
			:param sync: numeric
			:param bitcount: integer Range: 8 to 8
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sync', sync, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBX:BHConfig:SBYTe:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Sync: str: numeric
			- 2 Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Sync'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sync: str = None
			self.Bitcount: int = None

	def get(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:BHConfig:SBYTe:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dvb.dvbx.bhConfig.sbyte.pattern.get() \n
		Sets the user packet synchronization byte. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:DVB:DVBX:BHConfig:SBYTe:PATTern?', self.__class__.PatternStruct())
