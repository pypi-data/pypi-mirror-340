from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImmediateCls:
	"""Immediate commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("immediate", core, parent)

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:OFFSet \n
		Snippet: value: float = driver.source.power.level.immediate.get_offset() \n
		Sets the level offset of a downstream instrument. The level at the RF output is not changed. To query the resulting level,
		as it is at the output of the downstream instrument, use the command [:SOURce<hw>]:POWer[:LEVel][:IMMediate][:AMPLitude].
		See 'Displayed RF frequency and level values with downstream instruments'. Note: The level offset also affects the RF
		level sweep. \n
			:return: offset: float Range: -100 to 100 , Unit: dB Level offset is always expreced in dB; linear units (V, W, etc.) are not supported
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:OFFSet \n
		Snippet: driver.source.power.level.immediate.set_offset(offset = 1.0) \n
		Sets the level offset of a downstream instrument. The level at the RF output is not changed. To query the resulting level,
		as it is at the output of the downstream instrument, use the command [:SOURce<hw>]:POWer[:LEVel][:IMMediate][:AMPLitude].
		See 'Displayed RF frequency and level values with downstream instruments'. Note: The level offset also affects the RF
		level sweep. \n
			:param offset: float Range: -100 to 100 , Unit: dB Level offset is always expreced in dB; linear units (V, W, etc.) are not supported
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:OFFSet {param}')

	# noinspection PyTypeChecker
	def get_recall(self) -> enums.InclExcl:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:RCL \n
		Snippet: value: enums.InclExcl = driver.source.power.level.immediate.get_recall() \n
		Determines whether the current level is retained or if the stored level setting is adopted when an instrument
		configuration is loaded. The setting is valid for both paths. If a suffix is specified, it is ignored. \n
			:return: rcl: INCLude| EXCLude INCLude Takes the current level when an instrument configuration is loaded. EXCLude Retains the current level when an instrument configuration is loaded.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:RCL?')
		return Conversions.str_to_scalar_enum(response, enums.InclExcl)

	def set_recall(self, rcl: enums.InclExcl) -> None:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:RCL \n
		Snippet: driver.source.power.level.immediate.set_recall(rcl = enums.InclExcl.EXCLude) \n
		Determines whether the current level is retained or if the stored level setting is adopted when an instrument
		configuration is loaded. The setting is valid for both paths. If a suffix is specified, it is ignored. \n
			:param rcl: INCLude| EXCLude INCLude Takes the current level when an instrument configuration is loaded. EXCLude Retains the current level when an instrument configuration is loaded.
		"""
		param = Conversions.enum_scalar_to_str(rcl, enums.InclExcl)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:RCL {param}')

	def get_ref_level(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:REFLevel \n
		Snippet: value: float = driver.source.power.level.immediate.get_ref_level() \n
		Queries the reference level of the user correction. The reference level is the sum of the amplitude and the level offset,
		set with the commands [:SOURce<hw>]:POWer:POWer [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet. \n
			:return: reference_level: float Range: -245 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:REFLevel?')
		return Conversions.str_to_float(response)

	def set_ref_level(self, reference_level: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:REFLevel \n
		Snippet: driver.source.power.level.immediate.set_ref_level(reference_level = 1.0) \n
		Queries the reference level of the user correction. The reference level is the sum of the amplitude and the level offset,
		set with the commands [:SOURce<hw>]:POWer:POWer [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet. \n
			:param reference_level: float Range: -245 to 120
		"""
		param = Conversions.decimal_value_to_str(reference_level)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:REFLevel {param}')

	def get_amplitude(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:[AMPLitude] \n
		Snippet: value: float = driver.source.power.level.immediate.get_amplitude() \n
		Sets the RF level applied to the DUT. To activate the RF output use command method RsSmw.Output.State.value ('RF On'/'RF
		Off') .
			INTRO_CMD_HELP: The following applies POWer = RF output level + OFFSet, where: \n
			- POWer is the values set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate][:AMPLitude]
			- RF output level is set with [:SOURce<hw>]:POWer:POWer
			- OFFSet is set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet \n
			:return: amplitude: float The following settings influence the value range: OFFSet set with the command [:SOURcehw]:POWer[:LEVel][:IMMediate]:OFFSet Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command [:SOURcehw]:POWer:STEP[:INCRement]. Range: (Level_min + OFFSet) to (Level_max + OFFStet) , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, amplitude: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:[LEVel]:[IMMediate]:[AMPLitude] \n
		Snippet: driver.source.power.level.immediate.set_amplitude(amplitude = 1.0) \n
		Sets the RF level applied to the DUT. To activate the RF output use command method RsSmw.Output.State.value ('RF On'/'RF
		Off') .
			INTRO_CMD_HELP: The following applies POWer = RF output level + OFFSet, where: \n
			- POWer is the values set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate][:AMPLitude]
			- RF output level is set with [:SOURce<hw>]:POWer:POWer
			- OFFSet is set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet \n
			:param amplitude: float The following settings influence the value range: OFFSet set with the command [:SOURcehw]:POWer[:LEVel][:IMMediate]:OFFSet Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command [:SOURcehw]:POWer:STEP[:INCRement]. Range: (Level_min + OFFSet) to (Level_max + OFFStet) , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(amplitude)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:AMPLitude {param}')
