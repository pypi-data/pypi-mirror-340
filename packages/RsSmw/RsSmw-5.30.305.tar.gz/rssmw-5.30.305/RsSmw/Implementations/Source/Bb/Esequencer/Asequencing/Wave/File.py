from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ASEQuencing:WAVE:FILE:CATalog \n
		Snippet: value: List[str] = driver.source.bb.esequencer.asequencing.wave.file.get_catalog() \n
		Reads out the files extension *.wv in the default directory. \n
			:return: catalog: string Returns the available waveform files separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:ASEQuencing:WAVE:FILE:CATalog?')
		return Conversions.str_to_str_list(response)
