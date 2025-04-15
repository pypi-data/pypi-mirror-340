from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartupCls:
	"""Startup commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("startup", core, parent)

	def get_complete(self) -> bool:
		"""SCPI: SYSTem:STARtup:COMPlete \n
		Snippet: value: bool = driver.system.startup.get_complete() \n
		Queries if the startup of the instrument is completed. \n
			:return: complete: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SYSTem:STARtup:COMPlete?')
		return Conversions.str_to_bool(response)
