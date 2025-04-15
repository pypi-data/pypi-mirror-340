from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmsCls:
	"""Mms commands group definition. 14 total commands, 1 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mms", core, parent)

	@property
	def rsf(self):
		"""rsf commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_rsf'):
			from .Rsf import RsfCls
			self._rsf = RsfCls(self._core, self._cmd_group)
		return self._rsf

	# noinspection PyTypeChecker
	def get_mp_format(self) -> enums.HrpUwbMmsPktTyp:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:MPFormat \n
		Snippet: value: enums.HrpUwbMmsPktTyp = driver.source.bb.huwb.mms.get_mp_format() \n
		No command help available \n
			:return: mms_pkt_format: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:MPFormat?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMmsPktTyp)

	def set_mp_format(self, mms_pkt_format: enums.HrpUwbMmsPktTyp) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:MPFormat \n
		Snippet: driver.source.bb.huwb.mms.set_mp_format(mms_pkt_format = enums.HrpUwbMmsPktTyp.BOTH) \n
		No command help available \n
			:param mms_pkt_format: No help available
		"""
		param = Conversions.enum_scalar_to_str(mms_pkt_format, enums.HrpUwbMmsPktTyp)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:MPFormat {param}')

	# noinspection PyTypeChecker
	def get_nrif(self) -> enums.HrpUwbMmsrFragNumRif:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:NRIF \n
		Snippet: value: enums.HrpUwbMmsrFragNumRif = driver.source.bb.huwb.mms.get_nrif() \n
		No command help available \n
			:return: rif_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:NRIF?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMmsrFragNumRif)

	def set_nrif(self, rif_number: enums.HrpUwbMmsrFragNumRif) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:NRIF \n
		Snippet: driver.source.bb.huwb.mms.set_nrif(rif_number = enums.HrpUwbMmsrFragNumRif.FN0) \n
		No command help available \n
			:param rif_number: No help available
		"""
		param = Conversions.enum_scalar_to_str(rif_number, enums.HrpUwbMmsrFragNumRif)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:NRIF {param}')

	# noinspection PyTypeChecker
	def get_nrsf(self) -> enums.HrpUwbMmsrFragNumRsf:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:NRSF \n
		Snippet: value: enums.HrpUwbMmsrFragNumRsf = driver.source.bb.huwb.mms.get_nrsf() \n
		No command help available \n
			:return: rsf_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:NRSF?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMmsrFragNumRsf)

	def set_nrsf(self, rsf_number: enums.HrpUwbMmsrFragNumRsf) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:NRSF \n
		Snippet: driver.source.bb.huwb.mms.set_nrsf(rsf_number = enums.HrpUwbMmsrFragNumRsf.FN0) \n
		No command help available \n
			:param rsf_number: No help available
		"""
		param = Conversions.enum_scalar_to_str(rsf_number, enums.HrpUwbMmsrFragNumRsf)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:NRSF {param}')

	def get_ri_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RIOFfset \n
		Snippet: value: int = driver.source.bb.huwb.mms.get_ri_offset() \n
		No command help available \n
			:return: rif_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RIOFfset?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_role(self) -> enums.HrpUwbRangingRole:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:ROLE \n
		Snippet: value: enums.HrpUwbRangingRole = driver.source.bb.huwb.mms.get_role() \n
		No command help available \n
			:return: role: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbRangingRole)

	def set_role(self, role: enums.HrpUwbRangingRole) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:ROLE \n
		Snippet: driver.source.bb.huwb.mms.set_role(role = enums.HrpUwbRangingRole.INIT) \n
		No command help available \n
			:param role: No help available
		"""
		param = Conversions.enum_scalar_to_str(role, enums.HrpUwbRangingRole)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:ROLE {param}')

	def get_rp_duration(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RPDuration \n
		Snippet: value: int = driver.source.bb.huwb.mms.get_rp_duration() \n
		No command help available \n
			:return: rp_duration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RPDuration?')
		return Conversions.str_to_int(response)

	def set_rp_duration(self, rp_duration: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RPDuration \n
		Snippet: driver.source.bb.huwb.mms.set_rp_duration(rp_duration = 1) \n
		No command help available \n
			:param rp_duration: No help available
		"""
		param = Conversions.decimal_value_to_str(rp_duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RPDuration {param}')

	# noinspection PyTypeChecker
	def get_rs_duration(self) -> enums.HrpUwbMmsrSlotDur:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSDuration \n
		Snippet: value: enums.HrpUwbMmsrSlotDur = driver.source.bb.huwb.mms.get_rs_duration() \n
		No command help available \n
			:return: rs_duration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSDuration?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMmsrSlotDur)

	def set_rs_duration(self, rs_duration: enums.HrpUwbMmsrSlotDur) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSDuration \n
		Snippet: driver.source.bb.huwb.mms.set_rs_duration(rs_duration = enums.HrpUwbMmsrSlotDur.SD12) \n
		No command help available \n
			:param rs_duration: No help available
		"""
		param = Conversions.enum_scalar_to_str(rs_duration, enums.HrpUwbMmsrSlotDur)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RSDuration {param}')

	def get_rs_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSOFfset \n
		Snippet: value: int = driver.source.bb.huwb.mms.get_rs_offset() \n
		No command help available \n
			:return: rsf_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSOFfset?')
		return Conversions.str_to_int(response)

	def set_rs_offset(self, rsf_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSOFfset \n
		Snippet: driver.source.bb.huwb.mms.set_rs_offset(rsf_offset = 1) \n
		No command help available \n
			:param rsf_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(rsf_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RSOFfset {param}')

	def get_rstu(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSTU \n
		Snippet: value: int = driver.source.bb.huwb.mms.get_rstu() \n
		No command help available \n
			:return: rstu: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSTU?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_ssci(self) -> enums.HrpUwbCodeIndexSsci:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:SSCI \n
		Snippet: value: enums.HrpUwbCodeIndexSsci = driver.source.bb.huwb.mms.get_ssci() \n
		No command help available \n
			:return: ssci: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:SSCI?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbCodeIndexSsci)

	def set_ssci(self, ssci: enums.HrpUwbCodeIndexSsci) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:SSCI \n
		Snippet: driver.source.bb.huwb.mms.set_ssci(ssci = enums.HrpUwbCodeIndexSsci.CI_25) \n
		No command help available \n
			:param ssci: No help available
		"""
		param = Conversions.enum_scalar_to_str(ssci, enums.HrpUwbCodeIndexSsci)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:SSCI {param}')

	def get_tf_sync(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:TFSYnc \n
		Snippet: value: bool = driver.source.bb.huwb.mms.get_tf_sync() \n
		No command help available \n
			:return: time_freq_sync: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:TFSYnc?')
		return Conversions.str_to_bool(response)

	def set_tf_sync(self, time_freq_sync: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:TFSYnc \n
		Snippet: driver.source.bb.huwb.mms.set_tf_sync(time_freq_sync = False) \n
		No command help available \n
			:param time_freq_sync: No help available
		"""
		param = Conversions.bool_to_str(time_freq_sync)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:TFSYnc {param}')

	def clone(self) -> 'MmsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MmsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
