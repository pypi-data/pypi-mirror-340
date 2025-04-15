from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FptCls:
	"""Fpt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fpt", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MCS:FPT:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.mcs.fpt.get_state() \n
		Activates first path training. \n
			:return: fir_path_trning: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MCS:FPT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, fir_path_trning: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MCS:FPT:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.mcs.fpt.set_state(fir_path_trning = False) \n
		Activates first path training. \n
			:param fir_path_trning: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(fir_path_trning)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MCS:FPT:STATe {param}')
