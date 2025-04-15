from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClockCls:
	"""Clock commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocModeB:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:MODE \n
		Snippet: value: enums.ClocModeB = driver.source.bb.arbitrary.clock.get_mode() \n
		Enters the type of externally supplied clock. \n
			:return: mode: SAMPle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocModeB)

	def set_mode(self, mode: enums.ClocModeB) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:MODE \n
		Snippet: driver.source.bb.arbitrary.clock.set_mode(mode = enums.ClocModeB.MSAMple) \n
		Enters the type of externally supplied clock. \n
			:param mode: SAMPle
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocModeB)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:MULTiplier \n
		Snippet: value: int = driver.source.bb.arbitrary.clock.get_multiplier() \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, multiplier: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:MULTiplier \n
		Snippet: driver.source.bb.arbitrary.clock.set_multiplier(multiplier = 1) \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceC:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:SOURce \n
		Snippet: value: enums.ClockSourceC = driver.source.bb.arbitrary.clock.get_source() \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference
			- ELCLock: External local clock
			- EXTernal = ELCLock: Setting only Provided for backward compatibility with other Rohde & Schwarz signal generators \n
			:return: source: INTernal| ELCLock| EXTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceC)

	def set_source(self, source: enums.ClockSourceC) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:SOURce \n
		Snippet: driver.source.bb.arbitrary.clock.set_source(source = enums.ClockSourceC.ELCLock) \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference
			- ELCLock: External local clock
			- EXTernal = ELCLock: Setting only Provided for backward compatibility with other Rohde & Schwarz signal generators \n
			:param source: INTernal| ELCLock| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceC)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:SOURce {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk \n
		Snippet: value: float = driver.source.bb.arbitrary.clock.get_value() \n
		Sets the clock frequency. If you load a waveform, the clock rate is determined as defined with the waveform tag {CLOCK:
		frequency}. This command subsequently changes the clock rate; see specifications document for value range. In the case of
		an external clock source, the clock of the external source must be specified with this command. For more information,
		refer to the specifications document. \n
			:return: clock: float Range: depends on the installed options , Unit: Hz E.g. 400 Hz to 200 MHz (R&S SMW-B10)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk?')
		return Conversions.str_to_float(response)

	def set_value(self, clock: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk \n
		Snippet: driver.source.bb.arbitrary.clock.set_value(clock = 1.0) \n
		Sets the clock frequency. If you load a waveform, the clock rate is determined as defined with the waveform tag {CLOCK:
		frequency}. This command subsequently changes the clock rate; see specifications document for value range. In the case of
		an external clock source, the clock of the external source must be specified with this command. For more information,
		refer to the specifications document. \n
			:param clock: float Range: depends on the installed options , Unit: Hz E.g. 400 Hz to 200 MHz (R&S SMW-B10)
		"""
		param = Conversions.decimal_value_to_str(clock)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk {param}')
