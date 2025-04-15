from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:INPut:FREQuency \n
		Snippet: value: float = driver.source.efrontend.loscillator.inputPy.get_frequency() \n
		Requires [:SOURce<hw>]:EFRontend:LOSCillator:MODE EXTernal. Queries the required frequency on the 'LO In' connector of
		the connected external frontend. \n
			:return: lo_in_freq: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:LOSCillator:INPut:FREQuency?')
		return Conversions.str_to_float(response)
