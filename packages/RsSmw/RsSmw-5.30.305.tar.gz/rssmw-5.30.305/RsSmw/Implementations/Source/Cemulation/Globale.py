from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GlobaleCls:
	"""Globale commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("globale", core, parent)

	def get_seed(self) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:GLOBal:SEED \n
		Snippet: value: int = driver.source.cemulation.globale.get_seed() \n
		No command help available \n
			:return: seed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:GLOBal:SEED?')
		return Conversions.str_to_int(response)

	def set_seed(self, seed: int) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:GLOBal:SEED \n
		Snippet: driver.source.cemulation.globale.set_seed(seed = 1) \n
		No command help available \n
			:param seed: No help available
		"""
		param = Conversions.decimal_value_to_str(seed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:GLOBal:SEED {param}')
