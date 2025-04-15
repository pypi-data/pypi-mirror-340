from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MimoCls:
	"""Mimo commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mimo", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:MIMO:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.uconfig.mimo.get_state() \n
		Queries if the current user uses multi-user (MU) MIMO. All MU-MIMO users share one resource unit (RU) using different
		space time streams. \n
			:return: mimo_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:MIMO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mimo_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:MIMO:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.uconfig.mimo.set_state(mimo_state = False) \n
		Queries if the current user uses multi-user (MU) MIMO. All MU-MIMO users share one resource unit (RU) using different
		space time streams. \n
			:param mimo_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(mimo_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:MIMO:STATe {param}')
