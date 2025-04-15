from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AutoCls:
	"""Auto commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("auto", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:ILENgth:AUTO:[STATe] \n
		Snippet: value: bool = driver.source.bb.btooth.filterPy.ilength.auto.get_state() \n
		Activates the impulse length state. If activated, the most sensible parameter values are selected. The value depends on
		the coherence check. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:ILENgth:AUTO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:ILENgth:AUTO:[STATe] \n
		Snippet: driver.source.bb.btooth.filterPy.ilength.auto.set_state(state = False) \n
		Activates the impulse length state. If activated, the most sensible parameter values are selected. The value depends on
		the coherence check. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:FILTer:ILENgth:AUTO:STATe {param}')
