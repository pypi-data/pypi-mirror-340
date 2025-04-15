from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlevelCls:
	"""Alevel commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alevel", core, parent)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:VALue \n
		Snippet: value: float = driver.source.correction.fresponse.rf.user.alevel.get_value() \n
		Queries the absolute level correction value. Querying real values requires enabled absolute level compensation:
		SOURce1:CORRection:FRESponse:RF:USER:ALEVel:STATe 1 See also [:SOURce<hw>]:CORRection:FRESponse:RF:USER:ALEVel[:STATe]. \n
			:return: freq_cor_rf_absolute_val: float Range: -100 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:VALue?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:[STATe] \n
		Snippet: value: bool = driver.source.correction.fresponse.rf.user.alevel.get_state() \n
		Enables absolute level compensation at the current center frequency. Query the level correction value with the following
		command: [:SOURce<hw>]:CORRection:FRESponse:RF:USER:ALEVel:VALue? You cannot enable absolute level compensation and user
		correction simultaneously. These functions exclude each other. . \n
			:return: freq_corr_rf_al_sta: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_corr_rf_al_sta: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:[STATe] \n
		Snippet: driver.source.correction.fresponse.rf.user.alevel.set_state(freq_corr_rf_al_sta = False) \n
		Enables absolute level compensation at the current center frequency. Query the level correction value with the following
		command: [:SOURce<hw>]:CORRection:FRESponse:RF:USER:ALEVel:VALue? You cannot enable absolute level compensation and user
		correction simultaneously. These functions exclude each other. . \n
			:param freq_corr_rf_al_sta: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(freq_corr_rf_al_sta)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:STATe {param}')
