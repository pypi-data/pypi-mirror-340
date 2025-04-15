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

	def set_predefined(self, filename: str) -> None:
		"""SCPI: SCONfiguration:RFALignment:SETup:FILE:PREDefined \n
		Snippet: driver.sconfiguration.rfAlignment.setup.file.set_predefined(filename = 'abc') \n
		Loads the selected predefined file. \n
			:param filename: 'filename' File extension can be omitted. Query the filenames of predefined setup files with the command method RsSmw.Sconfiguration.RfAlignment.Setup.Predefined.catalog.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SCONfiguration:RFALignment:SETup:FILE:PREDefined {param}')

	def get_value(self) -> str:
		"""SCPI: SCONfiguration:RFALignment:SETup:FILE \n
		Snippet: value: str = driver.sconfiguration.rfAlignment.setup.file.get_value() \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.rfsa. \n
			:return: setup_file: 'filename' Filename or complete file path; file extension can be omitted. Query the filenames of existing setup files with the command method RsSmw.Sconfiguration.RfAlignment.Setup.catalog.
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:FILE?')
		return trim_str_response(response)

	def set_value(self, setup_file: str) -> None:
		"""SCPI: SCONfiguration:RFALignment:SETup:FILE \n
		Snippet: driver.sconfiguration.rfAlignment.setup.file.set_value(setup_file = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.rfsa. \n
			:param setup_file: 'filename' Filename or complete file path; file extension can be omitted. Query the filenames of existing setup files with the command method RsSmw.Sconfiguration.RfAlignment.Setup.catalog.
		"""
		param = Conversions.value_to_quoted_str(setup_file)
		self._core.io.write(f'SCONfiguration:RFALignment:SETup:FILE {param}')
