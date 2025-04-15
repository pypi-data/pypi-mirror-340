from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CextensionCls:
	"""Cextension commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cextension", core, parent)

	def get_pdelay(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:CEXTension:PDELay \n
		Snippet: value: float = driver.source.bbin.digital.cextension.get_pdelay() \n
		No command help available \n
			:return: processing_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:DIGital:CEXTension:PDELay?')
		return Conversions.str_to_float(response)

	def set_pdelay(self, processing_delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:CEXTension:PDELay \n
		Snippet: driver.source.bbin.digital.cextension.set_pdelay(processing_delay = 1.0) \n
		No command help available \n
			:param processing_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(processing_delay)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:DIGital:CEXTension:PDELay {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:CEXTension:STATe \n
		Snippet: value: bool = driver.source.bbin.digital.cextension.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:DIGital:CEXTension:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:CEXTension:STATe \n
		Snippet: driver.source.bbin.digital.cextension.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:DIGital:CEXTension:STATe {param}')
