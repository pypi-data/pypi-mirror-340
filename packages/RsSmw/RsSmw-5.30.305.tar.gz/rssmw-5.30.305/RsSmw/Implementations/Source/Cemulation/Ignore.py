from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IgnoreCls:
	"""Ignore commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ignore", core, parent)

	def get_rf_changes(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:IGNore:RFCHanges \n
		Snippet: value: bool = driver.source.cemulation.ignore.get_rf_changes() \n
		No command help available \n
			:return: rf_changes: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:IGNore:RFCHanges?')
		return Conversions.str_to_bool(response)

	def set_rf_changes(self, rf_changes: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:IGNore:RFCHanges \n
		Snippet: driver.source.cemulation.ignore.set_rf_changes(rf_changes = False) \n
		No command help available \n
			:param rf_changes: No help available
		"""
		param = Conversions.bool_to_str(rf_changes)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:IGNore:RFCHanges {param}')
