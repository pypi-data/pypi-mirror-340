from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModelingCls:
	"""Modeling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modeling", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:MODeling:[STATe] \n
		Snippet: value: bool = driver.source.cemulation.mimo.antenna.modeling.get_state() \n
		No command help available \n
			:return: antenna_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:ANTenna:MODeling:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, antenna_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:MODeling:[STATe] \n
		Snippet: driver.source.cemulation.mimo.antenna.modeling.set_state(antenna_state = False) \n
		No command help available \n
			:param antenna_state: No help available
		"""
		param = Conversions.bool_to_str(antenna_state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:ANTenna:MODeling:STATe {param}')
