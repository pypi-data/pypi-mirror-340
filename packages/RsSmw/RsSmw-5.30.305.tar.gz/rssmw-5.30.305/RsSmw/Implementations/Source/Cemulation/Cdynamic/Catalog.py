from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get_user(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:CATalog:USER \n
		Snippet: value: List[str] = driver.source.cemulation.cdynamic.catalog.get_user() \n
		No command help available \n
			:return: filenames: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CDYNamic:CATalog:USER?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:CATalog \n
		Snippet: value: List[str] = driver.source.cemulation.cdynamic.catalog.get_value() \n
		No command help available \n
			:return: filenames: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CDYNamic:CATalog?')
		return Conversions.str_to_str_list(response)
