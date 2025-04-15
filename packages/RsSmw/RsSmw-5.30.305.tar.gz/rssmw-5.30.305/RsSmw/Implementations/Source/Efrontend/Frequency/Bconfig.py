from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BconfigCls:
	"""Bconfig commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bconfig", core, parent)

	def get_auto(self) -> bool:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BCONfig:AUTO \n
		Snippet: value: bool = driver.source.efrontend.frequency.bconfig.get_auto() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:FREQuency:BCONfig:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, mode: bool) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BCONfig:AUTO \n
		Snippet: driver.source.efrontend.frequency.bconfig.set_auto(mode = False) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.bool_to_str(mode)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:FREQuency:BCONfig:AUTO {param}')
