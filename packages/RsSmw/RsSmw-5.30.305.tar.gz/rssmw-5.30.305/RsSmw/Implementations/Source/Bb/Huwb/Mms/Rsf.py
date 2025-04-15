from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsfCls:
	"""Rsf commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rsf", core, parent)

	# noinspection PyTypeChecker
	def get_mc_index(self) -> enums.HrpUwbCodeIndexRange:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MCINdex \n
		Snippet: value: enums.HrpUwbCodeIndexRange = driver.source.bb.huwb.mms.rsf.get_mc_index() \n
		No command help available \n
			:return: mmrs_code_index: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSF:MCINdex?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbCodeIndexRange)

	def set_mc_index(self, mmrs_code_index: enums.HrpUwbCodeIndexRange) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MCINdex \n
		Snippet: driver.source.bb.huwb.mms.rsf.set_mc_index(mmrs_code_index = enums.HrpUwbCodeIndexRange.CI_10) \n
		No command help available \n
			:param mmrs_code_index: No help available
		"""
		param = Conversions.enum_scalar_to_str(mmrs_code_index, enums.HrpUwbCodeIndexRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RSF:MCINdex {param}')

	def get_mcs_zeros(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MCSZeros \n
		Snippet: value: int = driver.source.bb.huwb.mms.rsf.get_mcs_zeros() \n
		No command help available \n
			:return: mcs_zeros: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSF:MCSZeros?')
		return Conversions.str_to_int(response)

	def set_mcs_zeros(self, mcs_zeros: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MCSZeros \n
		Snippet: driver.source.bb.huwb.mms.rsf.set_mcs_zeros(mcs_zeros = 1) \n
		No command help available \n
			:param mcs_zeros: No help available
		"""
		param = Conversions.decimal_value_to_str(mcs_zeros)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RSF:MCSZeros {param}')

	# noinspection PyTypeChecker
	def get_ms_repetition(self) -> enums.HrpUwbMmrsSymRepetition:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MSRepetition \n
		Snippet: value: enums.HrpUwbMmrsSymRepetition = driver.source.bb.huwb.mms.rsf.get_ms_repetition() \n
		No command help available \n
			:return: ms_repetition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:MMS:RSF:MSRepetition?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMmrsSymRepetition)

	def set_ms_repetition(self, ms_repetition: enums.HrpUwbMmrsSymRepetition) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:MMS:RSF:MSRepetition \n
		Snippet: driver.source.bb.huwb.mms.rsf.set_ms_repetition(ms_repetition = enums.HrpUwbMmrsSymRepetition.SR128) \n
		No command help available \n
			:param ms_repetition: No help available
		"""
		param = Conversions.enum_scalar_to_str(ms_repetition, enums.HrpUwbMmrsSymRepetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:MMS:RSF:MSRepetition {param}')
