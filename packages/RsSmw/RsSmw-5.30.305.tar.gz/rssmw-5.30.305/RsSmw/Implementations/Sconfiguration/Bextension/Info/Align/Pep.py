from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PepCls:
	"""Pep commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pep", core, parent)

	def get_maximum(self) -> float:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:PEP:MAXimum \n
		Snippet: value: float = driver.sconfiguration.bextension.info.align.pep.get_maximum() \n
		Queries the maximum peak envelope power (PEP) of the setup aligment procedure. Make sure, that the measurement device
		supports this power value. \n
			:return: max_pep: float Range: -145 to 30
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:PEP:MAXimum?')
		return Conversions.str_to_float(response)

	def get_minimum(self) -> float:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:PEP:MINimum \n
		Snippet: value: float = driver.sconfiguration.bextension.info.align.pep.get_minimum() \n
		Queries the start frequency of the setup aligment procedure. Make sure, that the measurement device supports this start
		frequency. \n
			:return: min_pep: float Range: -145 to 30
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:PEP:MINimum?')
		return Conversions.str_to_float(response)
