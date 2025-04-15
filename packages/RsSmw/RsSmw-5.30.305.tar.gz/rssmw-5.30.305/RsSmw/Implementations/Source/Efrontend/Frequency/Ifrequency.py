from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IfrequencyCls:
	"""Ifrequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ifrequency", core, parent)

	def get_side_band(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:IFRequency:SIDeband \n
		Snippet: value: str = driver.source.efrontend.frequency.ifrequency.get_side_band() \n
		Queries the currently used sideband for frequency conversion. \n
			:return: side_band: string USB Upper sideband LSB Lower sideband
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:FREQuency:IFRequency:SIDeband?')
		return trim_str_response(response)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:[FREQuency]:IFRequency:[VALue] \n
		Snippet: value: float = driver.source.efrontend.frequency.ifrequency.get_value() \n
		Queries the frequency of the IF signal, that is the frequency at the RF A/RF B connector. \n
			:return: int_frequency: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:FREQuency:IFRequency:VALue?')
		return Conversions.str_to_float(response)
