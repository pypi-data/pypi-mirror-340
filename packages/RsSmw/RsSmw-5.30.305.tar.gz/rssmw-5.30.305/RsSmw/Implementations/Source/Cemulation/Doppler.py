from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DopplerCls:
	"""Doppler commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("doppler", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.UnitFreqHzKhzMhzGhz:
		"""SCPI: [SOURce<HW>]:CEMulation:DOPPler:UNIT \n
		Snippet: value: enums.UnitFreqHzKhzMhzGhz = driver.source.cemulation.doppler.get_unit() \n
		No command help available \n
			:return: fad_dopp_freq_unit: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:DOPPler:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitFreqHzKhzMhzGhz)

	def set_unit(self, fad_dopp_freq_unit: enums.UnitFreqHzKhzMhzGhz) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:DOPPler:UNIT \n
		Snippet: driver.source.cemulation.doppler.set_unit(fad_dopp_freq_unit = enums.UnitFreqHzKhzMhzGhz.GHZ) \n
		No command help available \n
			:param fad_dopp_freq_unit: No help available
		"""
		param = Conversions.enum_scalar_to_str(fad_dopp_freq_unit, enums.UnitFreqHzKhzMhzGhz)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:DOPPler:UNIT {param}')
