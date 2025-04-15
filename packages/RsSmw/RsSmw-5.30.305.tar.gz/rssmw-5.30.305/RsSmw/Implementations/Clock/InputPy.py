from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: CLOCk:INPut:FREQuency \n
		Snippet: value: float = driver.clock.inputPy.get_frequency() \n
		Returns the measured frequency of the external clock signal. \n
			:return: frequency: float Range: 0 to max
		"""
		response = self._core.io.query_str('CLOCk:INPut:FREQuency?')
		return Conversions.str_to_float(response)
