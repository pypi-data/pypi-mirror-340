from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Year: int: integer Range: 1980 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get_date(self) -> DateStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:TIME:DATE \n
		Snippet: value: DateStruct = driver.source.bb.nr5G.trigger.time.get_date() \n
		Sets the date for a time-based trigger signal. For trigger modes single or armed auto, you can activate triggering at
		this date via the following command: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:STATe <DigStd> is the mnemonic for the digital
		standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support this feature. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:NR5G:TRIGger:TIME:DATE?', self.__class__.DateStruct())

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: int: integer Range: 0 to 59"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_int('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: int = None

	def get_time(self) -> TimeStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:TIME:TIME \n
		Snippet: value: TimeStruct = driver.source.bb.nr5G.trigger.time.get_time() \n
		Sets the time for a time-based trigger signal. For trigger modes single or armed auto, you can activate triggering at
		this time via the following command: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:STATe <DigStd> is the mnemonic for the digital
		standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support this feature. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:NR5G:TRIGger:TIME:TIME?', self.__class__.TimeStruct())

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:TIME:[STATe] \n
		Snippet: value: bool = driver.source.bb.nr5G.trigger.time.get_state() \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMW200A triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:TIME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:TIME:[STATe] \n
		Snippet: driver.source.bb.nr5G.trigger.time.set_state(state = False) \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMW200A triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:TIME:STATe {param}')
