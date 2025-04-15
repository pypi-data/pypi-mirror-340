from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScrewCls:
	"""Screw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("screw", core, parent)

	def get_position(self) -> int:
		"""SCPI: [SOURce<HW>]:EFRontend:SCRew:POSition \n
		Snippet: value: int = driver.source.efrontend.screw.get_position() \n
		No command help available \n
			:return: screw_position: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:SCRew:POSition?')
		return Conversions.str_to_int(response)
