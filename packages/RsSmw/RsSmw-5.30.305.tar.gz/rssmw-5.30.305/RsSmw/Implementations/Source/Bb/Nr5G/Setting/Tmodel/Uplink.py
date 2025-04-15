from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UplinkCls:
	"""Uplink commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uplink", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SETTing:TMODel:UL:CATalog \n
		Snippet: value: List[str] = driver.source.bb.nr5G.setting.tmodel.uplink.get_catalog() \n
		Queries the filenames of predefined files with test signals in the default directory. \n
			:return: nr_5_gcat_name_tmod_up: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:UL:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SETTing:TMODel:UL \n
		Snippet: value: str = driver.source.bb.nr5G.setting.tmodel.uplink.get_value() \n
		Loads a test model file with predefined settings. \n
			:return: tmod_up: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:UL?')
		return trim_str_response(response)
