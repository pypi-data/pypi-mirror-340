from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 6 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	@property
	def pconfiguration(self):
		"""pconfiguration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pconfiguration'):
			from .Pconfiguration import PconfigurationCls
			self._pconfiguration = PconfigurationCls(self._core, self._cmd_group)
		return self._pconfiguration

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.v5G.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.v5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: v_5_gcat_name: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def set_del_py(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:DEL \n
		Snippet: driver.source.bb.v5G.setting.set_del_py(filename = 'abc') \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.v5g. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: string Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:SETTing:DEL {param}')

	def get_load(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:LOAD \n
		Snippet: value: str = driver.source.bb.v5G.setting.get_load() \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.v5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:SETTing:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:LOAD \n
		Snippet: driver.source.bb.v5G.setting.set_load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.v5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:SETTing:LOAD {param}')

	def get_store(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:STORe \n
		Snippet: value: str = driver.source.bb.v5G.setting.get_store() \n
		Saves the current settings into the selected file; the file extension (*.v5g) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:SETTing:STORe?')
		return trim_str_response(response)

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:SETTing:STORe \n
		Snippet: driver.source.bb.v5G.setting.set_store(filename = 'abc') \n
		Saves the current settings into the selected file; the file extension (*.v5g) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:SETTing:STORe {param}')

	def clone(self) -> 'SettingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SettingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
