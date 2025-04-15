from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DptCls:
	"""Dpt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpt", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MCS:DPT:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.mcs.dpt.get_state() \n
		Activates dual polarisation TRN training. \n
			:return: dual_polar_trn: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MCS:DPT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, dual_polar_trn: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:MCS:DPT:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.mcs.dpt.set_state(dual_polar_trn = False) \n
		Activates dual polarisation TRN training. \n
			:param dual_polar_trn: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(dual_polar_trn)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:MCS:DPT:STATe {param}')
