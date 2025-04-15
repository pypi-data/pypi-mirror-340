from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 5 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	@property
	def tmodel(self):
		"""tmodel commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tmodel'):
			from .Tmodel import TmodelCls
			self._tmodel = TmodelCls(self._core, self._cmd_group)
		return self._tmodel

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.tdscdma.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.tdscdma. For general
		information on file handling in the default and in a specific directory, see section 'MMEMory Subsystem' in the R&S
		SMWuser manual. \n
			:return: catalog: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:SETTing:LOAD \n
		Snippet: driver.source.bb.tdscdma.setting.load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.tdscdma. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:SETTing:STORe \n
		Snippet: driver.source.bb.tdscdma.setting.set_store(filename = 'abc') \n
		Stores the current settings into the selected file; the file extension (*.tdscdma) is assigned automatically. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:SETTing:STORe {param}')

	def clone(self) -> 'SettingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SettingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
