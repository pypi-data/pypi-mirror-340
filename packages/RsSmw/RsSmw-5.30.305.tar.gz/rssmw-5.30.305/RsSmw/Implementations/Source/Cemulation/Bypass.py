from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BypassCls:
	"""Bypass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bypass", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:BYPass:STATe \n
		Snippet: value: bool = driver.source.cemulation.bypass.get_state() \n
		No command help available \n
			:return: byp_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BYPass:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, byp_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BYPass:STATe \n
		Snippet: driver.source.cemulation.bypass.set_state(byp_state = False) \n
		No command help available \n
			:param byp_state: No help available
		"""
		param = Conversions.bool_to_str(byp_state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BYPass:STATe {param}')
