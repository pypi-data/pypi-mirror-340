from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NucCls:
	"""Nuc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nuc", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:NUC:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.nuc.get_state() \n
		Activates nonuniform constellation (NUC) modulation. \n
			:return: nuc: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:NUC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, nuc: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:NUC:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.nuc.set_state(nuc = False) \n
		Activates nonuniform constellation (NUC) modulation. \n
			:param nuc: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(nuc)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:NUC:STATe {param}')
