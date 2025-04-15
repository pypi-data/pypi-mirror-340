from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 30 total commands, 7 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def arm(self):
		"""arm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arm'):
			from .Arm import ArmCls
			self._arm = ArmCls(self._core, self._cmd_group)
		return self._arm

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def obaseband(self):
		"""obaseband commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_obaseband'):
			from .Obaseband import ObasebandCls
			self._obaseband = ObasebandCls(self._core, self._cmd_group)
		return self._obaseband

	@property
	def output(self):
		"""output commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def external(self):
		"""external commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	def get_ptime(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:PTIMe \n
		Snippet: value: str = driver.source.bb.arbitrary.trigger.get_ptime() \n
		Queries the internal processing time. The processing time is the elapsed time between the input of the external trigger
		event and the output of the baseband signal. \n
			:return: arb_trig_proc_time: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:PTIMe?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.arbitrary.trigger.get_rmode() \n
		Queries the status of waveform output. \n
			:return: rmode: STOP| RUN RUN Outputs the waveform. A trigger event occurred in the triggered mode. STOP No waveform output. A trigger event did not occur in the triggered modes, or waveform output was stopped/armed.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.arbitrary.trigger.get_slength() \n
		Sets the length of the signal sequence that is output in the SINGle trigger mode. \n
			:return: slength: integer The maximum value depends on the selected units [:SOURcehw]:BB:ARBitrary:TRIGger:SLUNit as follows: SAMPle: Max = 232-1 SEQuence: Max = 1000 Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SLENgth \n
		Snippet: driver.source.bb.arbitrary.trigger.set_slength(slength = 1) \n
		Sets the length of the signal sequence that is output in the SINGle trigger mode. \n
			:param slength: integer The maximum value depends on the selected units [:SOURcehw]:BB:ARBitrary:TRIGger:SLUNit as follows: SAMPle: Max = 232-1 SEQuence: Max = 1000 Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlB:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SLUNit \n
		Snippet: value: enums.UnitSlB = driver.source.bb.arbitrary.trigger.get_sl_unit() \n
		Sets the unit for the entry of the length of the signal sequence to be output in the Single trigger mode. \n
			:return: sl_unit: SEQuence| SAMPle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlB)

	def set_sl_unit(self, sl_unit: enums.UnitSlB) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SLUNit \n
		Snippet: driver.source.bb.arbitrary.trigger.set_sl_unit(sl_unit = enums.UnitSlB.SAMPle) \n
		Sets the unit for the entry of the length of the signal sequence to be output in the Single trigger mode. \n
			:param sl_unit: SEQuence| SAMPle
		"""
		param = Conversions.enum_scalar_to_str(sl_unit, enums.UnitSlB)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.ArbTrigSegmModeNoEhop:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SMODe \n
		Snippet: value: enums.ArbTrigSegmModeNoEhop = driver.source.bb.arbitrary.trigger.get_smode() \n
		Selects the extended trigger mode for multi segment waveforms. \n
			:return: smode: SAME| NEXT| SEQuencer| NSEam NSEam = Next Segment Seamless
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ArbTrigSegmModeNoEhop)

	def set_smode(self, smode: enums.ArbTrigSegmModeNoEhop) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SMODe \n
		Snippet: driver.source.bb.arbitrary.trigger.set_smode(smode = enums.ArbTrigSegmModeNoEhop.NEXT) \n
		Selects the extended trigger mode for multi segment waveforms. \n
			:param smode: SAME| NEXT| SEQuencer| NSEam NSEam = Next Segment Seamless
		"""
		param = Conversions.enum_scalar_to_str(smode, enums.ArbTrigSegmModeNoEhop)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:SMODe {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceC:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SOURce \n
		Snippet: value: enums.TriggerSourceC = driver.source.bb.arbitrary.trigger.get_source() \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are the following trigger sources: \n
			- INTernal: Internal manual triggering of the instrument
			- INTA|INTB: Internal triggering by a signal from the other basebands
			- External trigger signal via one of the local or global connectors:
			Table Header:  \n
			- EGT1|EGT2: External global trigger
			- EGC1|EGC2: External global clock
			- ELTRigger: External local trigger
			- ELCLock: External local clock
			- For secondary instruments (SCONfiguration:MULTiinstrument:MODE SEC) , triggering
		via the external baseband synchronization signal of the primary instrument: SOURce1:BB:ARB:TRIGger:SOURce BBSY
			- OBASeband|BEXTernal|EXTernal: Setting only Provided only for backward
		compatibility with other Rohde & Schwarz signal generators. The R&S SMW200A accepts these values and maps them
		automatically as follows: EXTernal = EGT1, BEXTernal = EGT2, OBASeband = INTA or INTB (depending on the current baseband) \n
			:return: source: INTB| INTernal| OBASeband| EGT1| EGT2| EGC1| EGC2| ELTRigger| INTA| ELCLock| BEXTernal| EXTernal | BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceC)

	def set_source(self, source: enums.TriggerSourceC) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:SOURce \n
		Snippet: driver.source.bb.arbitrary.trigger.set_source(source = enums.TriggerSourceC.BBSY) \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are the following trigger sources: \n
			- INTernal: Internal manual triggering of the instrument
			- INTA|INTB: Internal triggering by a signal from the other basebands
			- External trigger signal via one of the local or global connectors:
			Table Header:  \n
			- EGT1|EGT2: External global trigger
			- EGC1|EGC2: External global clock
			- ELTRigger: External local trigger
			- ELCLock: External local clock
			- For secondary instruments (SCONfiguration:MULTiinstrument:MODE SEC) , triggering
		via the external baseband synchronization signal of the primary instrument: SOURce1:BB:ARB:TRIGger:SOURce BBSY
			- OBASeband|BEXTernal|EXTernal: Setting only Provided only for backward
		compatibility with other Rohde & Schwarz signal generators. The R&S SMW200A accepts these values and maps them
		automatically as follows: EXTernal = EGT1, BEXTernal = EGT2, OBASeband = INTA or INTB (depending on the current baseband) \n
			:param source: INTB| INTernal| OBASeband| EGT1| EGT2| EGC1| EGC2| ELTRigger| INTA| ELCLock| BEXTernal| EXTernal | BBSY
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceC)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.arbitrary.trigger.get_sequence() \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single
		See also 'About trigger modes'. \n
			:return: sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.arbitrary.trigger.set_sequence(sequence = enums.DmTrigMode.AAUTo) \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single
		See also 'About trigger modes'. \n
			:param sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:SEQuence {param}')

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
