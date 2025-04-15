from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DateCls:
	"""Date commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("date", core, parent)

	def set(self, year: int, month: int, day: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:DATE \n
		Snippet: driver.source.bb.gnss.time.start.date.set(year = 1, month = 1, day = 1) \n
		If the time base is UTC, defines the date for the simulation in DD.MM.YYYY format of the Gregorian calendar. \n
			:param year: integer Range: 1980 to 9999
			:param month: integer Range: 1 to 12
			:param day: integer Range: 1 to 31
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('year', year, DataType.Integer), ArgSingle('month', month, DataType.Integer), ArgSingle('day', day, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:DATE {param}'.rstrip())

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Year: int: integer Range: 1980 to 9999
			- 2 Month: int: integer Range: 1 to 12
			- 3 Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get(self) -> DateStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:DATE \n
		Snippet: value: DateStruct = driver.source.bb.gnss.time.start.date.get() \n
		If the time base is UTC, defines the date for the simulation in DD.MM.YYYY format of the Gregorian calendar. \n
			:return: structure: for return value, see the help for DateStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:DATE?', self.__class__.DateStruct())
