from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get(self, catalog_files: List[str]) -> List[str]:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BAND:CONFig:CATalog \n
		Snippet: value: List[str] = driver.source.efrontend.frequency.band.config.catalog.get(catalog_files = ['abc1', 'abc2', 'abc3']) \n
		Queries the selectable frequency band configuration modes. \n
			:param catalog_files: string Returns a string of selectable frequency band configuration modes separated by commas.
			:return: catalog_files: string Returns a string of selectable frequency band configuration modes separated by commas."""
		param = Conversions.list_to_csv_quoted_str(catalog_files)
		response = self._core.io.query_str(f'SOURce<HwInstance>:EFRontend:FREQuency:BAND:CONFig:CATalog? {param}')
		return Conversions.str_to_str_list(response)
