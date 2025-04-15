from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:PSEQuencer:FILE:CATalog \n
		Snippet: value: List[str] = driver.source.bb.esequencer.psequencer.file.get_catalog() \n
		Queries the available pulse sequencer files. As response, you get a string containing the existing files *.
		ps_def, separated by commas. To set the default directory, use command method RsSmw.MassMemory.currentDirectory. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:PSEQuencer:FILE:CATalog?')
		return Conversions.str_to_str_list(response)
