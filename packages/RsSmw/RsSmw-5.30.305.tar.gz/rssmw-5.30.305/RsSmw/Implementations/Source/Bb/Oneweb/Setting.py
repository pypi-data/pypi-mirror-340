from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.oneweb.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.ow.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_load(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:SETTing:LOAD \n
		Snippet: value: str = driver.source.bb.oneweb.setting.get_load() \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.ow.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:SETTing:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:SETTing:LOAD \n
		Snippet: driver.source.bb.oneweb.setting.set_load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.ow.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:SETTing:LOAD {param}')

	def get_store(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:SETTing:STORe \n
		Snippet: value: str = driver.source.bb.oneweb.setting.get_store() \n
		Saves the current settings into the selected file; the file extension (*.ow) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:SETTing:STORe?')
		return trim_str_response(response)

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:SETTing:STORe \n
		Snippet: driver.source.bb.oneweb.setting.set_store(filename = 'abc') \n
		Saves the current settings into the selected file; the file extension (*.ow) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:SETTing:STORe {param}')
