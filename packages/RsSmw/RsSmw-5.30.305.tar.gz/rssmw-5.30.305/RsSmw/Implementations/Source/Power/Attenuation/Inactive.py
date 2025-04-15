from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InactiveCls:
	"""Inactive commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inactive", core, parent)

	def get_indices(self) -> List[int]:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:INACtive:INDices \n
		Snippet: value: List[int] = driver.source.power.attenuation.inactive.get_indices() \n
		Queries inactive attenuations. Queries inactive attenuations. The response of the query returns the indices of the
		attenuations. \n
			:return: inactive_indices: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce<HwInstance>:POWer:ATTenuation:INACtive:INDices?')
		return response

	def set_indices(self, inactive_indices: List[int]) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:INACtive:INDices \n
		Snippet: driver.source.power.attenuation.inactive.set_indices(inactive_indices = [1, 2, 3]) \n
		Queries inactive attenuations. Queries inactive attenuations. The response of the query returns the indices of the
		attenuations. \n
			:param inactive_indices: No help available
		"""
		param = Conversions.list_to_csv_str(inactive_indices)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:INACtive:INDices {param}')
