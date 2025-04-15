from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_predefined(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:SETup:FILE:PREDefined \n
		Snippet: value: str = driver.sconfiguration.bextension.setup.file.get_predefined() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:SETup:FILE:PREDefined?')
		return trim_str_response(response)

	def set_predefined(self, filename: str) -> None:
		"""SCPI: SCONfiguration:BEXTension:SETup:FILE:PREDefined \n
		Snippet: driver.sconfiguration.bextension.setup.file.set_predefined(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SCONfiguration:BEXTension:SETup:FILE:PREDefined {param}')

	def get_value(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:SETup:FILE \n
		Snippet: value: str = driver.sconfiguration.bextension.setup.file.get_value() \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.bwsa. \n
			:return: setup_file: 'filename' Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:SETup:FILE?')
		return trim_str_response(response)

	def set_value(self, setup_file: str) -> None:
		"""SCPI: SCONfiguration:BEXTension:SETup:FILE \n
		Snippet: driver.sconfiguration.bextension.setup.file.set_value(setup_file = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.bwsa. \n
			:param setup_file: 'filename' Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(setup_file)
		self._core.io.write(f'SCONfiguration:BEXTension:SETup:FILE {param}')
