from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MuCls:
	"""Mu commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mu", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MU:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.mu.get_state() \n
		Queries the multi-user (MU) format state that is off. \n
			:return: mu_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MU:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mu_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MU:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.mu.set_state(mu_state = False) \n
		Queries the multi-user (MU) format state that is off. \n
			:param mu_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(mu_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MU:STATe {param}')
