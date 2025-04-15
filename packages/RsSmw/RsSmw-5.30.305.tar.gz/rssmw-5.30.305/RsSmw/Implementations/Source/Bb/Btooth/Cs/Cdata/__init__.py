from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdataCls:
	"""Cdata commands group definition. 51 total commands, 4 Subgroups, 44 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cdata", core, parent)

	@property
	def ccid(self):
		"""ccid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccid'):
			from .Ccid import CcidCls
			self._ccid = CcidCls(self._core, self._cmd_group)
		return self._ccid

	@property
	def ecode(self):
		"""ecode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecode'):
			from .Ecode import EcodeCls
			self._ecode = EcodeCls(self._core, self._cmd_group)
		return self._ecode

	@property
	def bposition(self):
		"""bposition commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bposition'):
			from .Bposition import BpositionCls
			self._bposition = BpositionCls(self._core, self._cmd_group)
		return self._bposition

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	# noinspection PyTypeChecker
	def get_aci(self) -> enums.BtoCsCtrlAci:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ACI \n
		Snippet: value: enums.BtoCsCtrlAci = driver.source.bb.btooth.cs.cdata.get_aci() \n
		Sets the antenna configuration index (ACI) field. The value has a length of 1 octet or 0 to 7 in decimal representation. \n
			:return: aci: ACI0| ACI1| ACI2| ACI3| ACI4| ACI5| ACI6| ACI7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ACI?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAci)

	def set_aci(self, aci: enums.BtoCsCtrlAci) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ACI \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_aci(aci = enums.BtoCsCtrlAci.ACI0) \n
		Sets the antenna configuration index (ACI) field. The value has a length of 1 octet or 0 to 7 in decimal representation. \n
			:param aci: ACI0| ACI1| ACI2| ACI3| ACI4| ACI5| ACI6| ACI7
		"""
		param = Conversions.enum_scalar_to_str(aci, enums.BtoCsCtrlAci)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ACI {param}')

	def get_ce_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CECount \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_ce_count() \n
		Sets the 16-bit connEventCount field bits in hexadecimal representation. \n
			:return: conn_event_count: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CECount?')
		return Conversions.str_to_int(response)

	def set_ce_count(self, conn_event_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CECount \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ce_count(conn_event_count = 1) \n
		Sets the 16-bit connEventCount field bits in hexadecimal representation. \n
			:param conn_event_count: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(conn_event_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CECount {param}')

	def get_cid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CID \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_cid() \n
		Sets the 6-bit Config_ID field that is the CS configuration ID. Settable ID values are 2 bits in decimal representation.
		All other values are for future use. \n
			:return: config_id: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CID?')
		return Conversions.str_to_int(response)

	def set_cid(self, config_id: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CID \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_cid(config_id = 1) \n
		Sets the 6-bit Config_ID field that is the CS configuration ID. Settable ID values are 2 bits in decimal representation.
		All other values are for future use. \n
			:param config_id: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(config_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CID {param}')

	def get_csa_threec(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSAThreec \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_csa_threec() \n
		Enables the channel selection algorithm #3c. \n
			:return: csa_threec: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSAThreec?')
		return Conversions.str_to_bool(response)

	def set_csa_threec(self, csa_threec: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSAThreec \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_csa_threec(csa_threec = False) \n
		Enables the channel selection algorithm #3c. \n
			:param csa_threec: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(csa_threec)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSAThreec {param}')

	def get_csignal(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSIGnal \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_csignal() \n
		Enables the companion signal. See also 'Companion Signal'. \n
			:return: companion_signal: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSIGnal?')
		return Conversions.str_to_bool(response)

	def set_csignal(self, companion_signal: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSIGnal \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_csignal(companion_signal = False) \n
		Enables the companion signal. See also 'Companion Signal'. \n
			:param companion_signal: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(companion_signal)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSIGnal {param}')

	# noinspection PyTypeChecker
	def get_csp_capability(self) -> enums.BtoCsCtrlSyncPhy:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSPCapability \n
		Snippet: value: enums.BtoCsCtrlSyncPhy = driver.source.bb.btooth.cs.cdata.get_csp_capability() \n
		Queries the value of the CS_SYNC_PHY_Capability field that is the LE 2M PHY. \n
			:return: sync_phy: LE2M
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSPCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlSyncPhy)

	def get_eoffset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:EOFFset \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_eoffset() \n
		Sets the time value of the Offset field. The value has a length of three octets or 9 bits. \n
			:return: event_offset: integer Range: 500 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:EOFFset?')
		return Conversions.str_to_int(response)

	def set_eoffset(self, event_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:EOFFset \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_eoffset(event_offset = 1) \n
		Sets the time value of the Offset field. The value has a length of three octets or 9 bits. \n
			:param event_offset: integer Range: 500 to 4e6
		"""
		param = Conversions.decimal_value_to_str(event_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:EOFFset {param}')

	def get_ma_path(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MAPath \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_ma_path() \n
		Sets the maximum Num_Ant paths. \n
			:return: max_ant_path: integer Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MAPath?')
		return Conversions.str_to_int(response)

	def set_ma_path(self, max_ant_path: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MAPath \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ma_path(max_ant_path = 1) \n
		Sets the maximum Num_Ant paths. \n
			:param max_ant_path: integer Range: 1 to 4
		"""
		param = Conversions.decimal_value_to_str(max_ant_path)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MAPath {param}')

	def get_mma_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMASteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mma_steps() \n
		Sets the maximum number of main mode steps. \n
			:return: mm_max_steps: integer Range: 2 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMASteps?')
		return Conversions.str_to_int(response)

	def set_mma_steps(self, mm_max_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMASteps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mma_steps(mm_max_steps = 1) \n
		Sets the maximum number of main mode steps. \n
			:param mm_max_steps: integer Range: 2 to 255
		"""
		param = Conversions.decimal_value_to_str(mm_max_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMASteps {param}')

	def get_mmi_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMISteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mmi_steps() \n
		Sets the minimum number of main mode steps. \n
			:return: mm_min_steps: integer Range: 2 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMISteps?')
		return Conversions.str_to_int(response)

	def set_mmi_steps(self, mm_min_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMISteps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mmi_steps(mm_min_steps = 1) \n
		Sets the minimum number of main mode steps. \n
			:param mm_min_steps: integer Range: 2 to 255
		"""
		param = Conversions.decimal_value_to_str(mm_min_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMISteps {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.BtoCsMainMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMODe \n
		Snippet: value: enums.BtoCsMainMode = driver.source.bb.btooth.cs.cdata.get_mmode() \n
		Sets the main mode of the CS LL Control PDU. For an overview on available submodes per main mode, see Table 'CS step main
		modes and submodes'. \n
			:return: main_mode: MODE1| MODE2| MODE3 For a description, see [:SOURcehw]:BB:BTOoth:CS[:SEVentch0]:MMODe.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsMainMode)

	def set_mmode(self, main_mode: enums.BtoCsMainMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mmode(main_mode = enums.BtoCsMainMode.MODE1) \n
		Sets the main mode of the CS LL Control PDU. For an overview on available submodes per main mode, see Table 'CS step main
		modes and submodes'. \n
			:param main_mode: MODE1| MODE2| MODE3 For a description, see [:SOURcehw]:BB:BTOoth:CS[:SEVentch0]:MMODe.
		"""
		param = Conversions.enum_scalar_to_str(main_mode, enums.BtoCsMainMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMODe {param}')

	def get_mm_repetition(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMRepetition \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mm_repetition() \n
		Sets the main mode repetition. \n
			:return: mm_repetition: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMRepetition?')
		return Conversions.str_to_int(response)

	def set_mm_repetition(self, mm_repetition: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMRepetition \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mm_repetition(mm_repetition = 1) \n
		Sets the main mode repetition. \n
			:param mm_repetition: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(mm_repetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMRepetition {param}')

	def get_mp_length(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPLength \n
		Snippet: value: float = driver.source.bb.btooth.cs.cdata.get_mp_length() \n
		Sets the time value of the Max_Procedure_Len field. The value has a length of two octets or 6 bits. \n
			:return: mp_length: float Range: 2.5 to 40959375
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPLength?')
		return Conversions.str_to_float(response)

	def set_mp_length(self, mp_length: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPLength \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mp_length(mp_length = 1.0) \n
		Sets the time value of the Max_Procedure_Len field. The value has a length of two octets or 6 bits. \n
			:param mp_length: float Range: 2.5 to 40959375
		"""
		param = Conversions.decimal_value_to_str(mp_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPLength {param}')

	def get_mp_supported(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPSupported \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mp_supported() \n
		Sets the bits of the Max_Procedures_Supported field. \n
			:return: mp_supported: integer Range: 0 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPSupported?')
		return Conversions.str_to_int(response)

	def set_mp_supported(self, mp_supported: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPSupported \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mp_supported(mp_supported = 1) \n
		Sets the bits of the Max_Procedures_Supported field. \n
			:param mp_supported: integer Range: 0 to 4
		"""
		param = Conversions.decimal_value_to_str(mp_supported)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPSupported {param}')

	# noinspection PyTypeChecker
	def get_mtype(self) -> enums.BtoCsCtrlModeType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MTYPe \n
		Snippet: value: enums.BtoCsCtrlModeType = driver.source.bb.btooth.cs.cdata.get_mtype() \n
		Queries the CS LL control packet mode type that is Mode-3. \n
			:return: mode_type: MODE3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlModeType)

	def get_mz_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MZSTeps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mz_steps() \n
		Sets the number of Mode-0 steps. \n
			:return: mode_0_steps: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MZSTeps?')
		return Conversions.str_to_int(response)

	def set_mz_steps(self, mode_0_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MZSTeps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mz_steps(mode_0_steps = 1) \n
		Sets the number of Mode-0 steps. \n
			:param mode_0_steps: integer Range: 1 to 3
		"""
		param = Conversions.decimal_value_to_str(mode_0_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MZSTeps {param}')

	def get_nant(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NANT \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_nant() \n
		Sets the bits of the Num_Ant field. This field indicates the number of antenna elements of the channel sounding device. \n
			:return: num_ant: integer Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NANT?')
		return Conversions.str_to_int(response)

	def set_nant(self, num_ant: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NANT \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nant(num_ant = 1) \n
		Sets the bits of the Num_Ant field. This field indicates the number of antenna elements of the channel sounding device. \n
			:param num_ant: integer Range: 1 to 4
		"""
		param = Conversions.decimal_value_to_str(num_ant)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NANT {param}')

	def get_nconfig(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NCONfig \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_nconfig() \n
		Sets the Num_Configs field that relates to the number of independent CS configurations. \n
			:return: num_config: integer Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NCONfig?')
		return Conversions.str_to_int(response)

	def set_nconfig(self, num_config: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NCONfig \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nconfig(num_config = 1) \n
		Sets the Num_Configs field that relates to the number of independent CS configurations. \n
			:param num_config: integer Range: 1 to 4
		"""
		param = Conversions.decimal_value_to_str(num_config)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NCONfig {param}')

	def get_nfae(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NFAE \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_nfae() \n
		Sets the No_FAE bit. This bit indicates if the transmitting LE device supports a fractional frequency offset actuation
		error (FAE) or not. \n
			:return: no_fae: 1| ON| 0| OFF 1|ON The transmitting LE device only supports an FAE of zero. 0|OFF The transmitting LE device supports FAE values as listed in an FAE table.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NFAE?')
		return Conversions.str_to_bool(response)

	def set_nfae(self, no_fae: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NFAE \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nfae(no_fae = False) \n
		Sets the No_FAE bit. This bit indicates if the transmitting LE device supports a fractional frequency offset actuation
		error (FAE) or not. \n
			:param no_fae: 1| ON| 0| OFF 1|ON The transmitting LE device only supports an FAE of zero. 0|OFF The transmitting LE device supports FAE values as listed in an FAE table.
		"""
		param = Conversions.bool_to_str(no_fae)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NFAE {param}')

	# noinspection PyTypeChecker
	def get_nrs_capability(self) -> enums.BtoCsCtrlNadm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NRSCapability \n
		Snippet: value: enums.BtoCsCtrlNadm = driver.source.bb.btooth.cs.cdata.get_nrs_capability() \n
		Sets the NADM random sequence capability. \n
			:return: nrs_capability: NONADM| NADM NONADM NADM disabled NADM NADM enabled
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NRSCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlNadm)

	def set_nrs_capability(self, nrs_capability: enums.BtoCsCtrlNadm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NRSCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nrs_capability(nrs_capability = enums.BtoCsCtrlNadm.NADM) \n
		Sets the NADM random sequence capability. \n
			:param nrs_capability: NONADM| NADM NONADM NADM disabled NADM NADM enabled
		"""
		param = Conversions.enum_scalar_to_str(nrs_capability, enums.BtoCsCtrlNadm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NRSCapability {param}')

	# noinspection PyTypeChecker
	def get_ns_capability(self) -> enums.BtoCsCtrlNadm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NSCapability \n
		Snippet: value: enums.BtoCsCtrlNadm = driver.source.bb.btooth.cs.cdata.get_ns_capability() \n
		Sets the NADM sounding sequence capability. \n
			:return: ns_capability: NONADM| NADM NONADM NADM disabled NADM NADM enabled
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NSCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlNadm)

	def set_ns_capability(self, ns_capability: enums.BtoCsCtrlNadm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NSCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ns_capability(ns_capability = enums.BtoCsCtrlNadm.NADM) \n
		Sets the NADM sounding sequence capability. \n
			:param ns_capability: NONADM| NADM NONADM NADM disabled NADM NADM enabled
		"""
		param = Conversions.enum_scalar_to_str(ns_capability, enums.BtoCsCtrlNadm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NSCapability {param}')

	def get_omax(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMAX \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_omax() \n
		Sets the time value of the Offset_Max field. The value has a length of 3 octets or 9 bits. \n
			:return: offset_max: integer Range: 500 to 16777215
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMAX?')
		return Conversions.str_to_int(response)

	def set_omax(self, offset_max: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMAX \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_omax(offset_max = 1) \n
		Sets the time value of the Offset_Max field. The value has a length of 3 octets or 9 bits. \n
			:param offset_max: integer Range: 500 to 16777215
		"""
		param = Conversions.decimal_value_to_str(offset_max)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMAX {param}')

	def get_omin(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMIN \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_omin() \n
		Sets the time value of the Offset_Min field. The value has a length of 3 octets or 9 bits. \n
			:return: offset_min: integer Range: 500 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMIN?')
		return Conversions.str_to_int(response)

	def set_omin(self, offset_min: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMIN \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_omin(offset_min = 1) \n
		Sets the time value of the Offset_Min field. The value has a length of 3 octets or 9 bits. \n
			:param offset_min: integer Range: 500 to 4e6
		"""
		param = Conversions.decimal_value_to_str(offset_min)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMIN {param}')

	def get_pcount(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PCOunt \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pcount() \n
		Sets the bits in the Procedure_Count field. The value has a length of 2 octets. \n
			:return: proc_count: integer Range: 1 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PCOunt?')
		return Conversions.str_to_int(response)

	def set_pcount(self, proc_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PCOunt \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pcount(proc_count = 1) \n
		Sets the bits in the Procedure_Count field. The value has a length of 2 octets. \n
			:param proc_count: integer Range: 1 to 65535
		"""
		param = Conversions.decimal_value_to_str(proc_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PCOunt {param}')

	def get_pdelta(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PDELta \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pdelta() \n
		Sets the bits in the Pwr_Delta field. The value has a length of 1 octets or 3 bits. \n
			:return: pwr_delta: integer Range: 0 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PDELta?')
		return Conversions.str_to_int(response)

	def set_pdelta(self, pwr_delta: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PDELta \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pdelta(pwr_delta = 1) \n
		Sets the bits in the Pwr_Delta field. The value has a length of 1 octets or 3 bits. \n
			:param pwr_delta: integer Range: 0 to 255
		"""
		param = Conversions.decimal_value_to_str(pwr_delta)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PDELta {param}')

	# noinspection PyTypeChecker
	def get_phy(self) -> enums.BtoPackFormat:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PHY \n
		Snippet: value: enums.BtoPackFormat = driver.source.bb.btooth.cs.cdata.get_phy() \n
		Queries the PHY field value. This value indicates the TX PHY of the remote device to which the Pwr_Delta field in this
		PDU applies. \n
			:return: phy: L1M| L2M| LCOD| L2M2B For a description, see [:SOURcehw]:BB:BTOoth:PFORmat.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PHY?')
		return Conversions.str_to_scalar_enum(response, enums.BtoPackFormat)

	def get_pinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pinterval() \n
		Sets the procedure interval in the Procedure_Interval field. The value has a length of two octets or 6 bits. \n
			:return: proc_interval: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PINTerval?')
		return Conversions.str_to_int(response)

	def set_pinterval(self, proc_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PINTerval \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pinterval(proc_interval = 1) \n
		Sets the procedure interval in the Procedure_Interval field. The value has a length of two octets or 6 bits. \n
			:param proc_interval: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(proc_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PINTerval {param}')

	# noinspection PyTypeChecker
	def get_pp_antenna(self) -> enums.BtoCsCtrlAnt:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PPANtenna \n
		Snippet: value: enums.BtoCsCtrlAnt = driver.source.bb.btooth.cs.cdata.get_pp_antenna() \n
		Sets the bits in the Preferred_Peer_Ant field. The value has a length of one octet or 3 bits.
		The table Table 'Preferred_Peer_Ant field values' lists all possible values and their meaning. \n
			:return: pp_antenna: ANT0| ANT1| ANT2| ANT3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PPANtenna?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAnt)

	def set_pp_antenna(self, pp_antenna: enums.BtoCsCtrlAnt) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PPANtenna \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pp_antenna(pp_antenna = enums.BtoCsCtrlAnt.ANT0) \n
		Sets the bits in the Preferred_Peer_Ant field. The value has a length of one octet or 3 bits.
		The table Table 'Preferred_Peer_Ant field values' lists all possible values and their meaning. \n
			:param pp_antenna: ANT0| ANT1| ANT2| ANT3
		"""
		param = Conversions.enum_scalar_to_str(pp_antenna, enums.BtoCsCtrlAnt)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PPANtenna {param}')

	# noinspection PyTypeChecker
	def get_ra_only(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RAONly \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_ra_only() \n
		Queries or sets the time values of the RTT_AA_Only_N field. Setting the value depends on the bits of the RTT_Capability
		field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit numbers and
		RTT fields' for an overview. \n
			:return: rtt_aa_only: AR150| AR10| AR0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RAONly?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_ra_only(self, rtt_aa_only: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RAONly \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ra_only(rtt_aa_only = enums.BtoCsCtrlAccReq.AR0) \n
		Queries or sets the time values of the RTT_AA_Only_N field. Setting the value depends on the bits of the RTT_Capability
		field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit numbers and
		RTT fields' for an overview. \n
			:param rtt_aa_only: AR150| AR10| AR0
		"""
		param = Conversions.enum_scalar_to_str(rtt_aa_only, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RAONly {param}')

	# noinspection PyTypeChecker
	def get_rcapability(self) -> enums.BtoCsCtrlRttCap:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RCAPability \n
		Snippet: value: enums.BtoCsCtrlRttCap = driver.source.bb.btooth.cs.cdata.get_rcapability() \n
		Sets the bits in the RTT_Capability field. These bits determine the time values for the RTT_AA_Only_N field, the
		RTT_Sounding_ N field and the RTT_Random_Sequence_N field. \n
			:return: rtt_capability: CAP0| CAP1| CAP2 See the table Table 'RTT_Capability bit numbers and RTT fields' for an overview.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RCAPability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlRttCap)

	def set_rcapability(self, rtt_capability: enums.BtoCsCtrlRttCap) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RCAPability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rcapability(rtt_capability = enums.BtoCsCtrlRttCap.CAP0) \n
		Sets the bits in the RTT_Capability field. These bits determine the time values for the RTT_AA_Only_N field, the
		RTT_Sounding_ N field and the RTT_Random_Sequence_N field. \n
			:param rtt_capability: CAP0| CAP1| CAP2 See the table Table 'RTT_Capability bit numbers and RTT fields' for an overview.
		"""
		param = Conversions.enum_scalar_to_str(rtt_capability, enums.BtoCsCtrlRttCap)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RCAPability {param}')

	def get_rfu(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RFU \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_rfu() \n
		Sets the bits that are reserved for future use (RFU) . The number of RFU bits can vary depending on the CS_Control_Data
		PDU. \n
			:return: rfu: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RFU?')
		return Conversions.str_to_int(response)

	def set_rfu(self, rfu: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RFU \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rfu(rfu = 1) \n
		Sets the bits that are reserved for future use (RFU) . The number of RFU bits can vary depending on the CS_Control_Data
		PDU. \n
			:param rfu: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(rfu)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RFU {param}')

	# noinspection PyTypeChecker
	def get_rr_sequence(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RRSequence \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_rr_sequence() \n
		Queries or sets the time values of the RTT_Random_Sequence_N field. Setting the value depends on the bits of the
		RTT_Capability field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit
		numbers and RTT fields' for an overview. \n
			:return: rr_sequence: AR150| AR10| AR0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RRSequence?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_rr_sequence(self, rr_sequence: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RRSequence \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rr_sequence(rr_sequence = enums.BtoCsCtrlAccReq.AR0) \n
		Queries or sets the time values of the RTT_Random_Sequence_N field. Setting the value depends on the bits of the
		RTT_Capability field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit
		numbers and RTT fields' for an overview. \n
			:param rr_sequence: AR150| AR10| AR0
		"""
		param = Conversions.enum_scalar_to_str(rr_sequence, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RRSequence {param}')

	# noinspection PyTypeChecker
	def get_rsounding(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RSOunding \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_rsounding() \n
		Queries or sets the time values of the RTT_Sounding_N field. Setting the value depends on the bits of the RTT_Capability
		field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit numbers and
		RTT fields' for an overview. \n
			:return: rsounding: AR150| AR10| AR0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RSOunding?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_rsounding(self, rsounding: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RSOunding \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rsounding(rsounding = enums.BtoCsCtrlAccReq.AR0) \n
		Queries or sets the time values of the RTT_Sounding_N field. Setting the value depends on the bits of the RTT_Capability
		field via the command: SOURce1:BB:BTOoth:CS:CDATa:RCAPability See also the table Table 'RTT_Capability bit numbers and
		RTT fields' for an overview. \n
			:param rsounding: AR150| AR10| AR0
		"""
		param = Conversions.enum_scalar_to_str(rsounding, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RSOunding {param}')

	# noinspection PyTypeChecker
	def get_rtype(self) -> enums.BtoCsCtrlRttType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RTYPe \n
		Snippet: value: enums.BtoCsCtrlRttType = driver.source.bb.btooth.cs.cdata.get_rtype() \n
		Sets the RTT type determined by the 4-bit RTT_Type field. This field indicates the round trip time (RTT) variant within
		the CS procedure. \n
			:return: rtt_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlRttType)

	def set_rtype(self, rtt_type: enums.BtoCsCtrlRttType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RTYPe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rtype(rtt_type = enums.BtoCsCtrlRttType.R128RS) \n
		Sets the RTT type determined by the 4-bit RTT_Type field. This field indicates the round trip time (RTT) variant within
		the CS procedure. \n
			:param rtt_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(rtt_type, enums.BtoCsCtrlRttType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RTYPe {param}')

	def get_sinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_sinterval() \n
		Sets or queries the subevent interval. Setting requires BB:BTOoth:CS:SNUMber 2 or higher.
		Query is for BB:BTOoth:CS:SNUMber 1. See [:SOURce<hw>]:BB:BTOoth:CS:CDATa:SNUMber. \n
			:return: sub_interval: integer Range: 0 to 2.7e11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SINTerval?')
		return Conversions.str_to_int(response)

	def set_sinterval(self, sub_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SINTerval \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_sinterval(sub_interval = 1) \n
		Sets or queries the subevent interval. Setting requires BB:BTOoth:CS:SNUMber 2 or higher.
		Query is for BB:BTOoth:CS:SNUMber 1. See [:SOURce<hw>]:BB:BTOoth:CS:CDATa:SNUMber. \n
			:param sub_interval: integer Range: 0 to 2.7e11
		"""
		param = Conversions.decimal_value_to_str(sub_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SINTerval {param}')

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SLENgth \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_slength() \n
		Sets the subevent length in the Subevent_Len field. The value has a length of three octets or 9 bits. \n
			:return: sub_length: integer Range: 1250 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, sub_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SLENgth \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_slength(sub_length = 1) \n
		Sets the subevent length in the Subevent_Len field. The value has a length of three octets or 9 bits. \n
			:param sub_length: integer Range: 1250 to 4e6
		"""
		param = Conversions.decimal_value_to_str(sub_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.BtoCsSubMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SMODe \n
		Snippet: value: enums.BtoCsSubMode = driver.source.bb.btooth.cs.cdata.get_smode() \n
		Sets the submode of the main mode. \n
			:return: sub_mode: MODE1| MODE2| MODE3| NONE See the table Table 'CS step main modes and submodes' for an overview on available submodes per main mode.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSubMode)

	def set_smode(self, sub_mode: enums.BtoCsSubMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SMODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_smode(sub_mode = enums.BtoCsSubMode.MODE1) \n
		Sets the submode of the main mode. \n
			:param sub_mode: MODE1| MODE2| MODE3| NONE See the table Table 'CS step main modes and submodes' for an overview on available submodes per main mode.
		"""
		param = Conversions.enum_scalar_to_str(sub_mode, enums.BtoCsSubMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SMODe {param}')

	def get_snumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SNUMber \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_snumber() \n
		Sets the number of subevents per event. \n
			:return: sub_number: integer Range: 1 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SNUMber?')
		return Conversions.str_to_int(response)

	def set_snumber(self, sub_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SNUMber \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_snumber(sub_number = 1) \n
		Sets the number of subevents per event. \n
			:param sub_number: integer Range: 1 to 32
		"""
		param = Conversions.decimal_value_to_str(sub_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SNUMber {param}')

	def get_sp_estimate(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SPEStimate \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_sp_estimate() \n
		Sets the Sounding_PCT_Estimate bit. This bit indicates if the device supports phase correction term (PCT) estimates from
		a sounding sequence or not. \n
			:return: sp_estimate: 1| ON| 0| OFF 1|ON The Sounding_PCT_Estimate bit is 1. The device supports PCT estimates from a sounding sequence. 0|OFF The Sounding_PCT_Estimate bit is 0. The device does not support PCT estimates from a sounding sequence.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SPEStimate?')
		return Conversions.str_to_bool(response)

	def set_sp_estimate(self, sp_estimate: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SPEStimate \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_sp_estimate(sp_estimate = False) \n
		Sets the Sounding_PCT_Estimate bit. This bit indicates if the device supports phase correction term (PCT) estimates from
		a sounding sequence or not. \n
			:param sp_estimate: 1| ON| 0| OFF 1|ON The Sounding_PCT_Estimate bit is 1. The device supports PCT estimates from a sounding sequence. 0|OFF The Sounding_PCT_Estimate bit is 0. The device does not support PCT estimates from a sounding sequence.
		"""
		param = Conversions.bool_to_str(sp_estimate)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SPEStimate {param}')

	# noinspection PyTypeChecker
	def get_tfcs(self) -> enums.BtoCsTfcs:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TFCS \n
		Snippet: value: enums.BtoCsTfcs = driver.source.bb.btooth.cs.cdata.get_tfcs() \n
		Sets the frequency change period (T_FCS) between consecutive CS steps. The period ranges from 15 us to 150 us. \n
			:return: tfcs: TFCS_15| TFCS_20| TFCS_30| TFCS_40| TFCS_50| TFCS_60| TFCS_80| TFCS_100| TFCS_120| TFCS_150 TFCS_x, x represents values in microseconds.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TFCS?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTfcs)

	def set_tfcs(self, tfcs: enums.BtoCsTfcs) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TFCS \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tfcs(tfcs = enums.BtoCsTfcs.TFCS_100) \n
		Sets the frequency change period (T_FCS) between consecutive CS steps. The period ranges from 15 us to 150 us. \n
			:param tfcs: TFCS_15| TFCS_20| TFCS_30| TFCS_40| TFCS_50| TFCS_60| TFCS_80| TFCS_100| TFCS_120| TFCS_150 TFCS_x, x represents values in microseconds.
		"""
		param = Conversions.enum_scalar_to_str(tfcs, enums.BtoCsTfcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TFCS {param}')

	# noinspection PyTypeChecker
	def get_ti_one(self) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TIONe \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.cdata.get_ti_one() \n
		Sets the time 'T_IP1' in microseconds. \n
			:return: tip_one: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145 TP1_x, x represents values in microseconds.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TIONe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)

	def set_ti_one(self, tip_one: enums.BtoCsTiP1) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TIONe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ti_one(tip_one = enums.BtoCsTiP1.TIP1_10) \n
		Sets the time 'T_IP1' in microseconds. \n
			:param tip_one: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145 TP1_x, x represents values in microseconds.
		"""
		param = Conversions.enum_scalar_to_str(tip_one, enums.BtoCsTiP1)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TIONe {param}')

	# noinspection PyTypeChecker
	def get_ti_two(self) -> enums.BtoCsTiP2:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TITWo \n
		Snippet: value: enums.BtoCsTiP2 = driver.source.bb.btooth.cs.cdata.get_ti_two() \n
		Sets the time 'T_IP2' in microseconds. \n
			:return: tip_two: TIP2_10| TIP2_20| TIP2_30| TIP2_40| TIP2_50| TIP2_60| TIP2_80| TIP2_145 TIP2_x, x represents values in microseconds.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TITWo?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP2)

	def set_ti_two(self, tip_two: enums.BtoCsTiP2) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TITWo \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ti_two(tip_two = enums.BtoCsTiP2.TIP2_10) \n
		Sets the time 'T_IP2' in microseconds. \n
			:param tip_two: TIP2_10| TIP2_20| TIP2_30| TIP2_40| TIP2_50| TIP2_60| TIP2_80| TIP2_145 TIP2_x, x represents values in microseconds.
		"""
		param = Conversions.enum_scalar_to_str(tip_two, enums.BtoCsTiP2)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TITWo {param}')

	# noinspection PyTypeChecker
	def get_tpm(self) -> enums.BtoCsTpm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TPM \n
		Snippet: value: enums.BtoCsTpm = driver.source.bb.btooth.cs.cdata.get_tpm() \n
		Sets the time 'T_PM' in microseconds. \n
			:return: tpm: TPM_10| TPM_20| TPM_40| TPM_652 TPM_x, x represents values in microseconds.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TPM?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTpm)

	def set_tpm(self, tpm: enums.BtoCsTpm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TPM \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tpm(tpm = enums.BtoCsTpm.TPM_10) \n
		Sets the time 'T_PM' in microseconds. \n
			:param tpm: TPM_10| TPM_20| TPM_40| TPM_652 TPM_x, x represents values in microseconds.
		"""
		param = Conversions.enum_scalar_to_str(tpm, enums.BtoCsTpm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TPM {param}')

	# noinspection PyTypeChecker
	def get_tsw(self) -> enums.BtoCsTsw:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TSW \n
		Snippet: value: enums.BtoCsTsw = driver.source.bb.btooth.cs.cdata.get_tsw() \n
		Sets the T_SW field values that relate to the duration of the antenna switch period. The local controller uses this
		period when switching antennas during active transmissions. \n
			:return: tsw: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10 Duration of the antenna switch period is 0, 1, 2, 4 or 10 microseconds.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TSW?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTsw)

	def set_tsw(self, tsw: enums.BtoCsTsw) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TSW \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tsw(tsw = enums.BtoCsTsw.TSW_0) \n
		Sets the T_SW field values that relate to the duration of the antenna switch period. The local controller uses this
		period when switching antennas during active transmissions. \n
			:param tsw: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10 Duration of the antenna switch period is 0, 1, 2, 4 or 10 microseconds.
		"""
		param = Conversions.enum_scalar_to_str(tsw, enums.BtoCsTsw)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TSW {param}')

	def clone(self) -> 'CdataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CdataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
