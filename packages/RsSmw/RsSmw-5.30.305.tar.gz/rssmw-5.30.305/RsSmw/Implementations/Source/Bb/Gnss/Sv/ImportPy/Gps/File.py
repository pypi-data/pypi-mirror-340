from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_constellation(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GPS:FILE:CONStellation \n
		Snippet: value: str = driver.source.bb.gnss.sv.importPy.gps.file.get_constellation() \n
		Selects the file from that the satellites constellation and navigation data are extracted. Supported file extensions for
		satellites constellation and navigation data
			Table Header: GNSS / File extension \n
			- GPS / *.rnx, *.txt, *.alm, *.al3, *.<xx>n,
			- Galileo / *.rnx, *.txt, *.alm, *.al3, *.<xx>n, *.<xx>l, *.xml
			- GLONASS / *.rnx, *.alg, *.<xx>n
			- BeiDou / *.rnx, *.txt, *.<xx>n, *.<xx>c
			- QZSS / *.rnx, *.txt, *.alm, *.<xx>n,
			- NavIC / *.rnx, *.<xx>i
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Filename, including file path and file extension.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:IMPort:GPS:FILE:CONStellation?')
		return trim_str_response(response)

	def set_constellation(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GPS:FILE:CONStellation \n
		Snippet: driver.source.bb.gnss.sv.importPy.gps.file.set_constellation(filename = 'abc') \n
		Selects the file from that the satellites constellation and navigation data are extracted. Supported file extensions for
		satellites constellation and navigation data
			Table Header: GNSS / File extension \n
			- GPS / *.rnx, *.txt, *.alm, *.al3, *.<xx>n,
			- Galileo / *.rnx, *.txt, *.alm, *.al3, *.<xx>n, *.<xx>l, *.xml
			- GLONASS / *.rnx, *.alg, *.<xx>n
			- BeiDou / *.rnx, *.txt, *.<xx>n, *.<xx>c
			- QZSS / *.rnx, *.txt, *.alm, *.<xx>n,
			- NavIC / *.rnx, *.<xx>i
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename, including file path and file extension.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GPS:FILE:CONStellation {param}')

	def get_nmessage(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GPS:FILE:NMESsage \n
		Snippet: value: str = driver.source.bb.gnss.sv.importPy.gps.file.get_nmessage() \n
		Selects the file from that the navigation data is extracted. For an overview of the supported file types, see Table
		'Supported file extensions for satellites constellation and navigation data'. Refer to 'Accessing Files in the Default or
		Specified Directory' for general information on file handling in the default and in a specific directory. \n
			:return: filename: string Filename, incl. file path and file extension.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:IMPort:GPS:FILE:NMESsage?')
		return trim_str_response(response)

	def set_nmessage(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GPS:FILE:NMESsage \n
		Snippet: driver.source.bb.gnss.sv.importPy.gps.file.set_nmessage(filename = 'abc') \n
		Selects the file from that the navigation data is extracted. For an overview of the supported file types, see Table
		'Supported file extensions for satellites constellation and navigation data'. Refer to 'Accessing Files in the Default or
		Specified Directory' for general information on file handling in the default and in a specific directory. \n
			:param filename: string Filename, incl. file path and file extension.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GPS:FILE:NMESsage {param}')
