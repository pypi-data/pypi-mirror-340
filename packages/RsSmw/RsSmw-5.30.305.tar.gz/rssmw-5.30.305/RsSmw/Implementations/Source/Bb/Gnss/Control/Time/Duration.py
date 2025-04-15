from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DurationCls:
	"""Duration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("duration", core, parent)

	def set(self, hour: int, minute: int, second: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:DURation \n
		Snippet: driver.source.bb.gnss.control.time.duration.set(hour = 1, minute = 1, second = 1) \n
		Sets the GNSS simulation duration of one repetition. After this period, the R&S SMW200A repeats the GNSS simulation or
		stops the GNSS simulation. To configure a repeated simulation, set the number of repetitions higher than one or disable
		repetitions for infinite repetition of the GNSS simulation. \n
			:param hour: integer Range: 0 to 240
			:param minute: integer Range: 0 to 59
			:param second: integer Range: 0 to 59
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('hour', hour, DataType.Integer), ArgSingle('minute', minute, DataType.Integer), ArgSingle('second', second, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:DURation {param}'.rstrip())

	# noinspection PyTypeChecker
	class DurationStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Hour: int: integer Range: 0 to 240
			- 2 Minute: int: integer Range: 0 to 59
			- 3 Second: int: integer Range: 0 to 59"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_int('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: int = None

	def get(self) -> DurationStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:CONTrol:TIME:DURation \n
		Snippet: value: DurationStruct = driver.source.bb.gnss.control.time.duration.get() \n
		Sets the GNSS simulation duration of one repetition. After this period, the R&S SMW200A repeats the GNSS simulation or
		stops the GNSS simulation. To configure a repeated simulation, set the number of repetitions higher than one or disable
		repetitions for infinite repetition of the GNSS simulation. \n
			:return: structure: for return value, see the help for DurationStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:CONTrol:TIME:DURation?', self.__class__.DurationStruct())
