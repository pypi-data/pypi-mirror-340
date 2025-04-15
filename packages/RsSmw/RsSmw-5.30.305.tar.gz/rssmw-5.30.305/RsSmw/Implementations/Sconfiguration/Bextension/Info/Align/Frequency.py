from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_maximum(self) -> float:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:FREQuency:MAXimum \n
		Snippet: value: float = driver.sconfiguration.bextension.info.align.frequency.get_maximum() \n
		Queries the end frequency of the setup aligment procedure. Make sure, that the measurement device supports this end
		frequency. \n
			:return: max_freq: float Range: 3.5E9 to 67E9
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:FREQuency:MAXimum?')
		return Conversions.str_to_float(response)

	def get_minimum(self) -> float:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:FREQuency:MINimum \n
		Snippet: value: float = driver.sconfiguration.bextension.info.align.frequency.get_minimum() \n
		Queries the start frequency of the setup aligment procedure. \n
			:return: min_freq: float Range: 3.5E9 to 67E9
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:FREQuency:MINimum?')
		return Conversions.str_to_float(response)
