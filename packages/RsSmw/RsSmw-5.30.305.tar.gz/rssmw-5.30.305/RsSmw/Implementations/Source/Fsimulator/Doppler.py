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
		"""SCPI: [SOURce<HW>]:FSIMulator:DOPPler:UNIT \n
		Snippet: value: enums.UnitFreqHzKhzMhzGhz = driver.source.fsimulator.doppler.get_unit() \n
		Sets the unit for the Doppler shift. Note that this setting only changes the Doppler unit in local mode. To set the speed
		units via remote control set the unit after the speed value. \n
			:return: fad_dopp_freq_unit: GHZ| MHZ| KHZ| HZ
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:DOPPler:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitFreqHzKhzMhzGhz)

	def set_unit(self, fad_dopp_freq_unit: enums.UnitFreqHzKhzMhzGhz) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DOPPler:UNIT \n
		Snippet: driver.source.fsimulator.doppler.set_unit(fad_dopp_freq_unit = enums.UnitFreqHzKhzMhzGhz.GHZ) \n
		Sets the unit for the Doppler shift. Note that this setting only changes the Doppler unit in local mode. To set the speed
		units via remote control set the unit after the speed value. \n
			:param fad_dopp_freq_unit: GHZ| MHZ| KHZ| HZ
		"""
		param = Conversions.enum_scalar_to_str(fad_dopp_freq_unit, enums.UnitFreqHzKhzMhzGhz)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:DOPPler:UNIT {param}')
