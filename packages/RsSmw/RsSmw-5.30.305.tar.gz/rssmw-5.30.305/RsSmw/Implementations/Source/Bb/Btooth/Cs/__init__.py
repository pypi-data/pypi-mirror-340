from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 109 total commands, 9 Subgroups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	@property
	def cdata(self):
		"""cdata commands group. 4 Sub-classes, 44 commands."""
		if not hasattr(self, '_cdata'):
			from .Cdata import CdataCls
			self._cdata = CdataCls(self._core, self._cmd_group)
		return self._cdata

	@property
	def cinc(self):
		"""cinc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cinc'):
			from .Cinc import CincCls
			self._cinc = CincCls(self._core, self._cmd_group)
		return self._cinc

	@property
	def cinp(self):
		"""cinp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cinp'):
			from .Cinp import CinpCls
			self._cinp = CinpCls(self._core, self._cmd_group)
		return self._cinp

	@property
	def civc(self):
		"""civc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_civc'):
			from .Civc import CivcCls
			self._civc = CivcCls(self._core, self._cmd_group)
		return self._civc

	@property
	def civp(self):
		"""civp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_civp'):
			from .Civp import CivpCls
			self._civp = CivpCls(self._core, self._cmd_group)
		return self._civp

	@property
	def cpvc(self):
		"""cpvc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpvc'):
			from .Cpvc import CpvcCls
			self._cpvc = CpvcCls(self._core, self._cmd_group)
		return self._cpvc

	@property
	def cpvp(self):
		"""cpvp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpvp'):
			from .Cpvp import CpvpCls
			self._cpvp = CpvpCls(self._core, self._cmd_group)
		return self._cpvp

	@property
	def correctionTable(self):
		"""correctionTable commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_correctionTable'):
			from .CorrectionTable import CorrectionTableCls
			self._correctionTable = CorrectionTableCls(self._core, self._cmd_group)
		return self._correctionTable

	@property
	def sevent(self):
		"""sevent commands group. 23 Sub-classes, 0 commands."""
		if not hasattr(self, '_sevent'):
			from .Sevent import SeventCls
			self._sevent = SeventCls(self._core, self._cmd_group)
		return self._sevent

	# noinspection PyTypeChecker
	class CfChmStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Cs_Filtered_Ch_M: str: numeric CSFilteredChM value in hexadecimal representation.
			- Bitcount: int: integer Fixed bit count of 80 bits. Range: 80 to 80"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_Filtered_Ch_M'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_Filtered_Ch_M: str = None
			self.Bitcount: int = None

	def get_cf_chm(self) -> CfChmStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CFCHm \n
		Snippet: value: CfChmStruct = driver.source.bb.btooth.cs.get_cf_chm() \n
		Queries the value of the field CSFilteredChM. This value determines the bit map for the Channel Sounding channel map
		update procedure. The parameter is 64-bit in hexadecimal representation. \n
			:return: structure: for return value, see the help for CfChmStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:CS:CFCHm?', self.__class__.CfChmStruct())

	def get_cinterval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINTerval \n
		Snippet: value: float = driver.source.bb.btooth.cs.get_cinterval() \n
		Sets the time of the LE connection interval. The anchor points of two consecutive CS events define the length of this
		interval. \n
			:return: connect_interval: float Range: 7.5 to 4000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CINTerval?')
		return Conversions.str_to_float(response)

	def set_cinterval(self, connect_interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_cinterval(connect_interval = 1.0) \n
		Sets the time of the LE connection interval. The anchor points of two consecutive CS events define the length of this
		interval. \n
			:param connect_interval: float Range: 7.5 to 4000
		"""
		param = Conversions.decimal_value_to_str(connect_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINTerval {param}')

	def get_cm_repetition(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CMRepetition \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_cm_repetition() \n
		Sets the 3-bit ChM_Repetition field. The value equals the number of cycles of the ChM field for non-Mode-0 steps within a
		CS procedure. \n
			:return: chm_repetition: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CMRepetition?')
		return Conversions.str_to_int(response)

	def set_cm_repetition(self, chm_repetition: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CMRepetition \n
		Snippet: driver.source.bb.btooth.cs.set_cm_repetition(chm_repetition = 1) \n
		Sets the 3-bit ChM_Repetition field. The value equals the number of cycles of the ChM field for non-Mode-0 steps within a
		CS procedure. \n
			:param chm_repetition: integer Range: 1 to 3
		"""
		param = Conversions.decimal_value_to_str(chm_repetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CMRepetition {param}')

	# noinspection PyTypeChecker
	def get_csel(self) -> enums.BtoCsChSel:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSEL \n
		Snippet: value: enums.BtoCsChSel = driver.source.bb.btooth.cs.get_csel() \n
		Sets the algorithm to select the channels. \n
			:return: ch_sel: SEL_3B| SEL_3C SEL_3B Sets for Algorithm #3b channel selection algorithm. SEL_3C Sets for Algorithm #3c channel selection algorithm. For related parameters, see Table 'Algorithm #3c parameters'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSEL?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsChSel)

	def set_csel(self, ch_sel: enums.BtoCsChSel) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSEL \n
		Snippet: driver.source.bb.btooth.cs.set_csel(ch_sel = enums.BtoCsChSel.SEL_3B) \n
		Sets the algorithm to select the channels. \n
			:param ch_sel: SEL_3B| SEL_3C SEL_3B Sets for Algorithm #3b channel selection algorithm. SEL_3C Sets for Algorithm #3c channel selection algorithm. For related parameters, see Table 'Algorithm #3c parameters'.
		"""
		param = Conversions.enum_scalar_to_str(ch_sel, enums.BtoCsChSel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSEL {param}')

	# noinspection PyTypeChecker
	def get_ctc_jump(self) -> enums.BtoCsCh3Cjump:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCJump \n
		Snippet: value: enums.BtoCsCh3Cjump = driver.source.bb.btooth.cs.get_ctc_jump() \n
		Determines the number of skipped channels when rendering the channel shapes. The Ch3cJump field has a length of 1 octet
		and relates to the channel index values. Configure this field when using the channel selection algorithm Algorithm #3c:
		SOURce1:BB:BTOoth:CS:CSEL SEL_3C \n
			:return: ch_three_cjump: JUMP_2| JUMP_3| JUMP_4| JUMP_5| JUMP_6| JUMP_7| JUMP_8 For Ch3cJump field parameters, see Table 'Algorithm #3c parameters'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CTCJump?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cjump)

	def set_ctc_jump(self, ch_three_cjump: enums.BtoCsCh3Cjump) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCJump \n
		Snippet: driver.source.bb.btooth.cs.set_ctc_jump(ch_three_cjump = enums.BtoCsCh3Cjump.JUMP_2) \n
		Determines the number of skipped channels when rendering the channel shapes. The Ch3cJump field has a length of 1 octet
		and relates to the channel index values. Configure this field when using the channel selection algorithm Algorithm #3c:
		SOURce1:BB:BTOoth:CS:CSEL SEL_3C \n
			:param ch_three_cjump: JUMP_2| JUMP_3| JUMP_4| JUMP_5| JUMP_6| JUMP_7| JUMP_8 For Ch3cJump field parameters, see Table 'Algorithm #3c parameters'.
		"""
		param = Conversions.enum_scalar_to_str(ch_three_cjump, enums.BtoCsCh3Cjump)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CTCJump {param}')

	# noinspection PyTypeChecker
	def get_ctc_shape(self) -> enums.BtoCsCh3Cshape:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCShape \n
		Snippet: value: enums.BtoCsCh3Cshape = driver.source.bb.btooth.cs.get_ctc_shape() \n
		Sets the bits of the Ch3cShape field. The field has a length of 4 bits and sets the shaping method of the rising and
		falling ramps of the channels. Configure this field when using the channel selection algorithm Algorithm #3c:
		SOURce1:BB:BTOoth:CS:CSEL SEL_3C \n
			:return: ch_three_cshape: HAT| X HAT Channel with a rising ramp and a falling ramp. X Channel with interleaved rising and falling ramps.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CTCShape?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cshape)

	def set_ctc_shape(self, ch_three_cshape: enums.BtoCsCh3Cshape) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCShape \n
		Snippet: driver.source.bb.btooth.cs.set_ctc_shape(ch_three_cshape = enums.BtoCsCh3Cshape.HAT) \n
		Sets the bits of the Ch3cShape field. The field has a length of 4 bits and sets the shaping method of the rising and
		falling ramps of the channels. Configure this field when using the channel selection algorithm Algorithm #3c:
		SOURce1:BB:BTOoth:CS:CSEL SEL_3C \n
			:param ch_three_cshape: HAT| X HAT Channel with a rising ramp and a falling ramp. X Channel with interleaved rising and falling ramps.
		"""
		param = Conversions.enum_scalar_to_str(ch_three_cshape, enums.BtoCsCh3Cshape)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CTCShape {param}')

	def get_einterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_einterval() \n
		Sets the number of LE connection event intervals. \n
			:return: event_interval: integer Range: 1 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EINTerval?')
		return Conversions.str_to_int(response)

	def set_einterval(self, event_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_einterval(event_interval = 1) \n
		Sets the number of LE connection event intervals. \n
			:param event_interval: integer Range: 1 to 65535
		"""
		param = Conversions.decimal_value_to_str(event_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EINTerval {param}')

	def get_eoffset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EOFFset \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_eoffset() \n
		Sets the time between the anchor point of the LE connection event and the beginning of the CS event. If you select manual
		step scheduling, you can set event offsets lower than 500 microseconds. An offset of 0 microseconds means that the CS
		event starts at the anchor point of the LE connection event. \n
			:return: event_offset: integer Range: 500 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EOFFset?')
		return Conversions.str_to_int(response)

	def set_eoffset(self, event_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EOFFset \n
		Snippet: driver.source.bb.btooth.cs.set_eoffset(event_offset = 1) \n
		Sets the time between the anchor point of the LE connection event and the beginning of the CS event. If you select manual
		step scheduling, you can set event offsets lower than 500 microseconds. An offset of 0 microseconds means that the CS
		event starts at the anchor point of the LE connection event. \n
			:param event_offset: integer Range: 500 to 4e6
		"""
		param = Conversions.decimal_value_to_str(event_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EOFFset {param}')

	def get_ntfcs(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:NTFCs \n
		Snippet: value: bool = driver.source.bb.btooth.cs.get_ntfcs() \n
		Enables setting of a zero frequency change period (T_FCS) in the first CS step. \n
			:return: no_tfcs: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:NTFCs?')
		return Conversions.str_to_bool(response)

	def set_ntfcs(self, no_tfcs: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:NTFCs \n
		Snippet: driver.source.bb.btooth.cs.set_ntfcs(no_tfcs = False) \n
		Enables setting of a zero frequency change period (T_FCS) in the first CS step. \n
			:param no_tfcs: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(no_tfcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:NTFCs {param}')

	# noinspection PyTypeChecker
	def get_role(self) -> enums.BtoCsRoles:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: value: enums.BtoCsRoles = driver.source.bb.btooth.cs.get_role() \n
		Sets the role of the channel sounding device that is the R&S SMW200A. \n
			:return: role: INITiator| REFLector INITiator The instrument initiates a CS procedure. REFLector The instrument responds to a CS procedure.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsRoles)

	def set_role(self, role: enums.BtoCsRoles) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: driver.source.bb.btooth.cs.set_role(role = enums.BtoCsRoles.INITiator) \n
		Sets the role of the channel sounding device that is the R&S SMW200A. \n
			:param role: INITiator| REFLector INITiator The instrument initiates a CS procedure. REFLector The instrument responds to a CS procedure.
		"""
		param = Conversions.enum_scalar_to_str(role, enums.BtoCsRoles)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:ROLE {param}')

	def get_sinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_sinterval() \n
		Sets the subevent interval. This interval is the time in multiples of 625 us between the beginning of a CS subevent and
		the beginning of the next CS subevent within the same CS event. For SOURce1:BB:BTO:CS:SNUM 1, the subevent interval is
		0us. For SOURce1:BB:BTO:CS:SNUM 2 or higher, settable subevent intervals depend on the number of event intervals, the
		connection interval, the event offset and the subevent length. See also [:SOURce<hw>]:BB:BTOoth:CS:SNUMber. \n
			:return: sub_interval: integer Range: 0 to 2.7e11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SINTerval?')
		return Conversions.str_to_int(response)

	def set_sinterval(self, sub_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_sinterval(sub_interval = 1) \n
		Sets the subevent interval. This interval is the time in multiples of 625 us between the beginning of a CS subevent and
		the beginning of the next CS subevent within the same CS event. For SOURce1:BB:BTO:CS:SNUM 1, the subevent interval is
		0us. For SOURce1:BB:BTO:CS:SNUM 2 or higher, settable subevent intervals depend on the number of event intervals, the
		connection interval, the event offset and the subevent length. See also [:SOURce<hw>]:BB:BTOoth:CS:SNUMber. \n
			:param sub_interval: integer Range: 0 to 2.7e11
		"""
		param = Conversions.decimal_value_to_str(sub_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SINTerval {param}')

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SLENgth \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_slength() \n
		Sets the subevent length that is the duration of a CS subevent. You can set values in multiples of 625 us.
		Settable subevent lengths depend on the number of event intervals, the connection interval, the event offset and the
		subevent interval. \n
			:return: sub_length: integer Range: 1250 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, sub_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SLENgth \n
		Snippet: driver.source.bb.btooth.cs.set_slength(sub_length = 1) \n
		Sets the subevent length that is the duration of a CS subevent. You can set values in multiples of 625 us.
		Settable subevent lengths depend on the number of event intervals, the connection interval, the event offset and the
		subevent interval. \n
			:param sub_length: integer Range: 1250 to 4e6
		"""
		param = Conversions.decimal_value_to_str(sub_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SLENgth {param}')

	def get_snumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SNUMber \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_snumber() \n
		Sets number of subevents. Settable values depend on the subevent interval. \n
			:return: sub_number: integer Range: 1 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SNUMber?')
		return Conversions.str_to_int(response)

	def set_snumber(self, sub_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SNUMber \n
		Snippet: driver.source.bb.btooth.cs.set_snumber(sub_number = 1) \n
		Sets number of subevents. Settable values depend on the subevent interval. \n
			:param sub_number: integer Range: 1 to 32
		"""
		param = Conversions.decimal_value_to_str(sub_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SNUMber {param}')

	# noinspection PyTypeChecker
	def get_sscheduling(self) -> enums.AutoManualMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SSCHeduling \n
		Snippet: value: enums.AutoManualMode = driver.source.bb.btooth.cs.get_sscheduling() \n
		Sets the step scheduling mode. \n
			:return: step_scheduling: AUTO| MANual AUTO Automatic CS step scheduling. The subevent length, the subevent interval and the number of subevents are configurable. The number of CS steps is 2. MANual Manual CS step scheduling. The subevent length is 1250 us, the subevent interval is 0 us and the number of subevents is 1. The number of CS steps is configurable.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SSCHeduling?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_sscheduling(self, step_scheduling: enums.AutoManualMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SSCHeduling \n
		Snippet: driver.source.bb.btooth.cs.set_sscheduling(step_scheduling = enums.AutoManualMode.AUTO) \n
		Sets the step scheduling mode. \n
			:param step_scheduling: AUTO| MANual AUTO Automatic CS step scheduling. The subevent length, the subevent interval and the number of subevents are configurable. The number of CS steps is 2. MANual Manual CS step scheduling. The subevent length is 1250 us, the subevent interval is 0 us and the number of subevents is 1. The number of CS steps is configurable.
		"""
		param = Conversions.enum_scalar_to_str(step_scheduling, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SSCHeduling {param}')

	def clone(self) -> 'CsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
