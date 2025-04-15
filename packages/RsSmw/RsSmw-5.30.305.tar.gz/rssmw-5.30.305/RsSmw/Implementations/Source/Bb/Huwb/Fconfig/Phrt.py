from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhrtCls:
	"""Phrt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phrt", core, parent)

	# noinspection PyTypeChecker
	def get_bitrate(self) -> enums.HrpUwbPhr2BitRate:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:PHRT:BITRate \n
		Snippet: value: enums.HrpUwbPhr2BitRate = driver.source.bb.huwb.fconfig.phrt.get_bitrate() \n
		No command help available \n
			:return: phr_2_bit_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:PHRT:BITRate?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbPhr2BitRate)

	def set_bitrate(self, phr_2_bit_rate: enums.HrpUwbPhr2BitRate) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:PHRT:BITRate \n
		Snippet: driver.source.bb.huwb.fconfig.phrt.set_bitrate(phr_2_bit_rate = enums.HrpUwbPhr2BitRate.R124M8) \n
		No command help available \n
			:param phr_2_bit_rate: No help available
		"""
		param = Conversions.enum_scalar_to_str(phr_2_bit_rate, enums.HrpUwbPhr2BitRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:PHRT:BITRate {param}')
