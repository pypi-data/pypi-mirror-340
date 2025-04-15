from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	# noinspection PyTypeChecker
	def get_fh_mode(self) -> enums.UlFreqHopMode:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:FHMode \n
		Snippet: value: enums.UlFreqHopMode = driver.source.bb.oneweb.uplink.pusch.get_fh_mode() \n
		No command help available \n
			:return: freq_hopping_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:FHMode?')
		return Conversions.str_to_scalar_enum(response, enums.UlFreqHopMode)

	def set_fh_mode(self, freq_hopping_mode: enums.UlFreqHopMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:FHMode \n
		Snippet: driver.source.bb.oneweb.uplink.pusch.set_fh_mode(freq_hopping_mode = enums.UlFreqHopMode.INTer) \n
		No command help available \n
			:param freq_hopping_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(freq_hopping_mode, enums.UlFreqHopMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:FHMode {param}')

	def get_fh_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:FHOFfset \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.pusch.get_fh_offset() \n
		No command help available \n
			:return: fhopp_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:FHOFfset?')
		return Conversions.str_to_int(response)

	def set_fh_offset(self, fhopp_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:FHOFfset \n
		Snippet: driver.source.bb.oneweb.uplink.pusch.set_fh_offset(fhopp_offset = 1) \n
		No command help available \n
			:param fhopp_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(fhopp_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:FHOFfset {param}')

	def get_nosm(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:NOSM \n
		Snippet: value: int = driver.source.bb.oneweb.uplink.pusch.get_nosm() \n
		No command help available \n
			:return: sub_band_count: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:NOSM?')
		return Conversions.str_to_int(response)

	def set_nosm(self, sub_band_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:PUSCh:NOSM \n
		Snippet: driver.source.bb.oneweb.uplink.pusch.set_nosm(sub_band_count = 1) \n
		No command help available \n
			:param sub_band_count: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_band_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UL:PUSCh:NOSM {param}')
