from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsetCls:
	"""Cset commands group definition. 14 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cset", core, parent)

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce]:CORRection:CSET:CATalog \n
		Snippet: value: List[str] = driver.source.correction.cset.get_catalog() \n
		Queries a list of available user correction tables. \n
			:return: catalog: string List of list filenames, separated by commas
		"""
		response = self._core.io.query_str('SOURce:CORRection:CSET:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce]:CORRection:CSET:DELete \n
		Snippet: driver.source.correction.cset.delete(filename = 'abc') \n
		Deletes the specified user correction list file. \n
			:param filename: string Filename or complete file path; file extension is optional.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce:CORRection:CSET:DELete {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:[SELect] \n
		Snippet: value: str = driver.source.correction.cset.get_select() \n
		Selects or creates a file for the user correction data. If the file with the selected name does not exist, a new file is
		created. \n
			:return: filename: string Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:CSET:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:[SELect] \n
		Snippet: driver.source.correction.cset.set_select(filename = 'abc') \n
		Selects or creates a file for the user correction data. If the file with the selected name does not exist, a new file is
		created. \n
			:param filename: string Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:SELect {param}')

	def clone(self) -> 'CsetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
