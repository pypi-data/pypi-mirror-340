from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PathCls:
	"""Path commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("path", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:MODulation:PATH:[STATe] \n
		Snippet: value: bool = driver.source.modulation.path.get_state() \n
		No command help available \n
			:return: mod_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:MODulation:PATH:STATe?')
		return Conversions.str_to_bool(response)
