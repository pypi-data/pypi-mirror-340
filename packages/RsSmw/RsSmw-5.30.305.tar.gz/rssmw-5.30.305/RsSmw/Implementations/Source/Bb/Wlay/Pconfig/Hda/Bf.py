from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BfCls:
	"""Bf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bf", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BF:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.bf.get_state() \n
		If activated, applies digital beamforming. \n
			:return: beamforming: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BF:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, beamforming: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BF:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.bf.set_state(beamforming = False) \n
		If activated, applies digital beamforming. \n
			:param beamforming: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(beamforming)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BF:STATe {param}')
