from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	def get_bfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FILTer:BFACtor \n
		Snippet: value: float = driver.source.bb.nr5G.output.filterPy.get_bfactor() \n
		No command help available \n
			:return: bw_factor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FILTer:BFACtor?')
		return Conversions.str_to_float(response)

	def get_bw_2_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FILTer:BW2Factor \n
		Snippet: value: float = driver.source.bb.nr5G.output.filterPy.get_bw_2_factor() \n
		No command help available \n
			:return: band_2_factor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FILTer:BW2Factor?')
		return Conversions.str_to_float(response)

	def get_custom(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FILTer:CUSTom \n
		Snippet: value: bool = driver.source.bb.nr5G.output.filterPy.get_custom() \n
		No command help available \n
			:return: use_custom: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FILTer:CUSTom?')
		return Conversions.str_to_bool(response)

	def set_custom(self, use_custom: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FILTer:CUSTom \n
		Snippet: driver.source.bb.nr5G.output.filterPy.set_custom(use_custom = False) \n
		No command help available \n
			:param use_custom: No help available
		"""
		param = Conversions.bool_to_str(use_custom)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:FILTer:CUSTom {param}')

	def get_tabs(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FILTer:TABS \n
		Snippet: value: int = driver.source.bb.nr5G.output.filterPy.get_tabs() \n
		No command help available \n
			:return: filter_tabs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FILTer:TABS?')
		return Conversions.str_to_int(response)
