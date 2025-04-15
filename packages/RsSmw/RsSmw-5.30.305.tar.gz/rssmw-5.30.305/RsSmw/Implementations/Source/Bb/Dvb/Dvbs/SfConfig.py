from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfConfigCls:
	"""SfConfig commands group definition. 17 total commands, 0 Subgroups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfConfig", core, parent)

	def get_csf_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:CSFLength \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_csf_length() \n
		Requires more than one super frame as set via the command SOURce1:sBB:DVB:DVBS|DVBX:SFBHconfig:NOSF.
		Queries the calculated super frame length in symbols. \n
			:return: calculated_sfl: integer Range: 8856 to 612540
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:CSFLength?')
		return Conversions.str_to_int(response)

	def get_cu_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:CULength \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_cu_length() \n
		Queries the capacity unit length. \n
			:return: cu_length: integer Range: 90 to 90
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:CULength?')
		return Conversions.str_to_int(response)

	def get_dsf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:DSF \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_dsf() \n
		Queries the distance between super frame start and start of pilot field in the super frame. \n
			:return: pilot_filed_dis: integer Range: 1440 to 1440
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:DSF?')
		return Conversions.str_to_int(response)

	def get_ehf_size(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:EHFSize \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_ehf_size() \n
		Requires [:SOURce<hw>]:BB:DVB:DVBS|DVBX:SFBHconfig:STATe 1 and [:SOURce<hw>]:BB:DVB:DVBS|DVBX:SFConfig:SFFI SFFI6.
		Queries the extended header filed (EHF) size. \n
			:return: ehf_size: integer Range: 504 to 504
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:EHFSize?')
		return Conversions.str_to_int(response)

	def get_npay(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:NPAY \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_npay() \n
		Sets the scrambling code number for the payload data scrambler. \n
			:return: npay: integer Range: 0 to 1048574
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:NPAY?')
		return Conversions.str_to_int(response)

	def set_npay(self, npay: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:NPAY \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_npay(npay = 1) \n
		Sets the scrambling code number for the payload data scrambler. \n
			:param npay: integer Range: 0 to 1048574
		"""
		param = Conversions.decimal_value_to_str(npay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:NPAY {param}')

	def get_nref(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:NREF \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_nref() \n
		Sets the scrambling code number for the reference data scrambler. \n
			:return: nref: integer Range: 0 to 1048574
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:NREF?')
		return Conversions.str_to_int(response)

	def set_nref(self, nref: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:NREF \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_nref(nref = 1) \n
		Sets the scrambling code number for the reference data scrambler. \n
			:param nref: integer Range: 0 to 1048574
		"""
		param = Conversions.decimal_value_to_str(nref)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:NREF {param}')

	def get_plength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PLENgth \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_plength() \n
		Queries the postamble length. \n
			:return: postamble_length: integer Range: 90 to 900
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PLENgth?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_pli(self) -> enums.DvbS2Xsfpli:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PLI \n
		Snippet: value: enums.DvbS2Xsfpli = driver.source.bb.dvb.dvbs.sfConfig.get_pli() \n
		Selects the protection level indicator of the physical layer header. \n
			:return: pli: STD| ROB| VROB| HEFF STD Standard protection of physical layer header using BPSK with spreding factor 1. ROB Robust protection of physical layer header using BPSK with spreding factor 2. VROB Very robust protection of physical layer header using BPSK with spreding factor 5. HEFF High efficiency protection of physical layer header using QPSK with punctering. The selection applies only for 8PSK and higher MODCOD schemes refer to payload transfer.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PLI?')
		return Conversions.str_to_scalar_enum(response, enums.DvbS2Xsfpli)

	def set_pli(self, pli: enums.DvbS2Xsfpli) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PLI \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_pli(pli = enums.DvbS2Xsfpli.HEFF) \n
		Selects the protection level indicator of the physical layer header. \n
			:param pli: STD| ROB| VROB| HEFF STD Standard protection of physical layer header using BPSK with spreding factor 1. ROB Robust protection of physical layer header using BPSK with spreding factor 2. VROB Very robust protection of physical layer header using BPSK with spreding factor 5. HEFF High efficiency protection of physical layer header using QPSK with punctering. The selection applies only for 8PSK and higher MODCOD schemes refer to payload transfer.
		"""
		param = Conversions.enum_scalar_to_str(pli, enums.DvbS2Xsfpli)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PLI {param}')

	def get_psf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PSF \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_psf() \n
		Queries the pilot field size. \n
			:return: pilot_field_size: integer Range: 36 to 36
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PSF?')
		return Conversions.str_to_int(response)

	def get_pstate(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PSTate \n
		Snippet: value: bool = driver.source.bb.dvb.dvbs.sfConfig.get_pstate() \n
		Sets the super frame pilot active. \n
			:return: sf_pilot_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PSTate?')
		return Conversions.str_to_bool(response)

	def set_pstate(self, sf_pilot_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PSTate \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_pstate(sf_pilot_state = False) \n
		Sets the super frame pilot active. \n
			:param sf_pilot_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(sf_pilot_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PSTate {param}')

	def get_pwh(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PWH \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_pwh() \n
		Sets the super frame pilot Walsh-Hadamard (WH) sequence set. \n
			:return: sf_pilot_wh: integer Range: 0 to 31
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PWH?')
		return Conversions.str_to_int(response)

	def set_pwh(self, sf_pilot_wh: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:PWH \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_pwh(sf_pilot_wh = 1) \n
		Sets the super frame pilot Walsh-Hadamard (WH) sequence set. \n
			:param sf_pilot_wh: integer Range: 0 to 31
		"""
		param = Conversions.decimal_value_to_str(sf_pilot_wh)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:PWH {param}')

	# noinspection PyTypeChecker
	def get_sffi(self) -> enums.DvbS2XsfFormat:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SFFI \n
		Snippet: value: enums.DvbS2XsfFormat = driver.source.bb.dvb.dvbs.sfConfig.get_sffi() \n
		Sets the super frame format indicator to a value coinside with format 0 to format 7. \n
			:return: sffi: SFFI4| SFFI5| SFFI6| SFFI7 SFFI4 Requires deactivated beam hopping. Sets a fixed super frame length. SFFI5 Define a custom super frame length. SFFI6 to SFFI7 Requires activated beam hopping. Define a customized super frame length with activated beam hopping.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SFFI?')
		return Conversions.str_to_scalar_enum(response, enums.DvbS2XsfFormat)

	def set_sffi(self, sffi: enums.DvbS2XsfFormat) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SFFI \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_sffi(sffi = enums.DvbS2XsfFormat.SFFI0) \n
		Sets the super frame format indicator to a value coinside with format 0 to format 7. \n
			:param sffi: SFFI4| SFFI5| SFFI6| SFFI7 SFFI4 Requires deactivated beam hopping. Sets a fixed super frame length. SFFI5 Define a custom super frame length. SFFI6 to SFFI7 Requires activated beam hopping. Define a customized super frame length with activated beam hopping.
		"""
		param = Conversions.enum_scalar_to_str(sffi, enums.DvbS2XsfFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SFFI {param}')

	def get_sf_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SFLength \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_sf_length() \n
		Sets the super frame length. SFFI 0 to 3 are not supported. For SFFI = 5 to 7, the command sets the superframe length.
		For SFFI = 4, this command is for query only. \n
			:return: sf_length: integer Range: 8856 to 612540
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SFLength?')
		return Conversions.str_to_int(response)

	def set_sf_length(self, sf_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SFLength \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_sf_length(sf_length = 1) \n
		Sets the super frame length. SFFI 0 to 3 are not supported. For SFFI = 5 to 7, the command sets the superframe length.
		For SFFI = 4, this command is for query only. \n
			:param sf_length: integer Range: 8856 to 612540
		"""
		param = Conversions.decimal_value_to_str(sf_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SFLength {param}')

	def get_sosf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SOSF \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_sosf() \n
		Sets the start of super frame Walsh-Hadamard (WH) sequence. \n
			:return: sosf: integer Range: 0 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SOSF?')
		return Conversions.str_to_int(response)

	def set_sosf(self, sosf: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:SOSF \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_sosf(sosf = 1) \n
		Sets the start of super frame Walsh-Hadamard (WH) sequence. \n
			:param sosf: integer Range: 0 to 255
		"""
		param = Conversions.decimal_value_to_str(sosf)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:SOSF {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:STATe \n
		Snippet: value: bool = driver.source.bb.dvb.dvbs.sfConfig.get_state() \n
		Activates the super frame. \n
			:return: sf_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sf_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:STATe \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_state(sf_state = False) \n
		Activates the super frame. \n
			:param sf_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(sf_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:STATe {param}')

	def get_stwh(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:STWH \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_stwh() \n
		The super frame trailer (ST) extends the frame field in respect of the super frame header (SFH) with a Walsh-Hadamard
		(WH) sequence. \n
			:return: st: integer Range: 0 to 63
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:STWH?')
		return Conversions.str_to_int(response)

	def set_stwh(self, st: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:STWH \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_stwh(st = 1) \n
		The super frame trailer (ST) extends the frame field in respect of the super frame header (SFH) with a Walsh-Hadamard
		(WH) sequence. \n
			:param st: integer Range: 0 to 63
		"""
		param = Conversions.decimal_value_to_str(st)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:STWH {param}')

	def get_tsn(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:TSN \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfConfig.get_tsn() \n
		Sets the time slice number (TSN) . The TSN is identified in the wideband header. The TSN information determines which
		physical layer frames the receiver decodes and which frames the receiver discards. \n
			:return: tsn: integer Range: 0 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:TSN?')
		return Conversions.str_to_int(response)

	def set_tsn(self, tsn: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFConfig:TSN \n
		Snippet: driver.source.bb.dvb.dvbs.sfConfig.set_tsn(tsn = 1) \n
		Sets the time slice number (TSN) . The TSN is identified in the wideband header. The TSN information determines which
		physical layer frames the receiver decodes and which frames the receiver discards. \n
			:param tsn: integer Range: 0 to 255
		"""
		param = Conversions.decimal_value_to_str(tsn)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFConfig:TSN {param}')
