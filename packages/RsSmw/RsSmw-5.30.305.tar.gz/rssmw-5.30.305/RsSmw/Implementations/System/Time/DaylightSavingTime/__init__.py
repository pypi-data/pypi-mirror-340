from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaylightSavingTimeCls:
	"""DaylightSavingTime commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("daylightSavingTime", core, parent)

	@property
	def rule(self):
		"""rule commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rule'):
			from .Rule import RuleCls
			self._rule = RuleCls(self._core, self._cmd_group)
		return self._rule

	def get_mode(self) -> str:
		"""SCPI: SYSTem:TIME:DSTime:MODE \n
		Snippet: value: str = driver.system.time.daylightSavingTime.get_mode() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:DSTime:MODE?')
		return trim_str_response(response)

	def set_mode(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:TIME:DSTime:MODE \n
		Snippet: driver.system.time.daylightSavingTime.set_mode(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:DSTime:MODE {param}')

	def clone(self) -> 'DaylightSavingTimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DaylightSavingTimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
