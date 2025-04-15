from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PathCls:
	"""Path commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("path", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:FSIMulator:HSTRain:PATH:STATe \n
		Snippet: value: bool = driver.source.fsimulator.hsTrain.path.get_state() \n
		Activates/deactivates the selected path for the High Speed Train fading configurations. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:HSTRain:PATH:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:HSTRain:PATH:STATe \n
		Snippet: driver.source.fsimulator.hsTrain.path.set_state(state = False) \n
		Activates/deactivates the selected path for the High Speed Train fading configurations. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:HSTRain:PATH:STATe {param}')
