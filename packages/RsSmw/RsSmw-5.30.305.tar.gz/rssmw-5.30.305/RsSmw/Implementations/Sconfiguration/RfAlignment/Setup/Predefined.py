from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PredefinedCls:
	"""Predefined commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("predefined", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: SCONfiguration:RFALignment:SETup:PREDefined:CATalog \n
		Snippet: value: List[str] = driver.sconfiguration.rfAlignment.setup.predefined.get_catalog() \n
		Queries the names of the existing predefined setup files. Only files with extension *.rfsa are listed. \n
			:return: rf_port_setup_file_cat_name_predefined: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:PREDefined:CATalog?')
		return Conversions.str_to_str_list(response)
