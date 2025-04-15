from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StbcCls:
	"""Stbc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stbc", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:STBC:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.stbc.get_state() \n
		Queries the state of space-time block coding that is off. \n
			:return: stbc: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:STBC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, stbc: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:STBC:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.stbc.set_state(stbc = False) \n
		Queries the state of space-time block coding that is off. \n
			:param stbc: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(stbc)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:STBC:STATe {param}')
