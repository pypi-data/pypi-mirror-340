from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:DELay \n
		Snippet: value: float = driver.source.cemulation.mdelay.reference.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:REFerence:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:DELay \n
		Snippet: driver.source.cemulation.mdelay.reference.set_delay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:REFerence:DELay {param}')

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:LOSS \n
		Snippet: value: float = driver.source.cemulation.mdelay.reference.get_loss() \n
		No command help available \n
			:return: loss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:REFerence:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:LOSS \n
		Snippet: driver.source.cemulation.mdelay.reference.set_loss(loss = 1.0) \n
		No command help available \n
			:param loss: No help available
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:REFerence:LOSS {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:STATe \n
		Snippet: value: bool = driver.source.cemulation.mdelay.reference.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:REFerence:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:REFerence:STATe \n
		Snippet: driver.source.cemulation.mdelay.reference.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:REFerence:STATe {param}')
