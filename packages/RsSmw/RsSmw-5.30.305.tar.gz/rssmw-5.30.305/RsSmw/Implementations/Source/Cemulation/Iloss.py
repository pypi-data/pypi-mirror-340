from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IlossCls:
	"""Iloss commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iloss", core, parent)

	def get_csamples(self) -> str:
		"""SCPI: [SOURce<HW>]:CEMulation:ILOSs:CSAMples \n
		Snippet: value: str = driver.source.cemulation.iloss.get_csamples() \n
		No command help available \n
			:return: csamples: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:ILOSs:CSAMples?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FadInsLossMode:
		"""SCPI: [SOURce<HW>]:CEMulation:ILOSs:MODE \n
		Snippet: value: enums.FadInsLossMode = driver.source.cemulation.iloss.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:ILOSs:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FadInsLossMode)

	def set_mode(self, mode: enums.FadInsLossMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:ILOSs:MODE \n
		Snippet: driver.source.cemulation.iloss.set_mode(mode = enums.FadInsLossMode.LACP) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FadInsLossMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:ILOSs:MODE {param}')

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:ILOSs:[LOSS] \n
		Snippet: value: float = driver.source.cemulation.iloss.get_loss() \n
		No command help available \n
			:return: loss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:ILOSs:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:ILOSs:[LOSS] \n
		Snippet: driver.source.cemulation.iloss.set_loss(loss = 1.0) \n
		No command help available \n
			:param loss: No help available
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:ILOSs:LOSS {param}')
