from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LogNormalCls:
	"""LogNormal commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("logNormal", core, parent)

	def get_cstd(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:COUPle:LOGNormal:CSTD \n
		Snippet: value: bool = driver.source.cemulation.couple.logNormal.get_cstd() \n
		No command help available \n
			:return: cstd: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:COUPle:LOGNormal:CSTD?')
		return Conversions.str_to_bool(response)

	def set_cstd(self, cstd: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:COUPle:LOGNormal:CSTD \n
		Snippet: driver.source.cemulation.couple.logNormal.set_cstd(cstd = False) \n
		No command help available \n
			:param cstd: No help available
		"""
		param = Conversions.bool_to_str(cstd)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:COUPle:LOGNormal:CSTD {param}')

	def get_lconstant(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:COUPle:LOGNormal:LCONstant \n
		Snippet: value: bool = driver.source.cemulation.couple.logNormal.get_lconstant() \n
		No command help available \n
			:return: lconstant: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:COUPle:LOGNormal:LCONstant?')
		return Conversions.str_to_bool(response)

	def set_lconstant(self, lconstant: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:COUPle:LOGNormal:LCONstant \n
		Snippet: driver.source.cemulation.couple.logNormal.set_lconstant(lconstant = False) \n
		No command help available \n
			:param lconstant: No help available
		"""
		param = Conversions.bool_to_str(lconstant)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:COUPle:LOGNormal:LCONstant {param}')
