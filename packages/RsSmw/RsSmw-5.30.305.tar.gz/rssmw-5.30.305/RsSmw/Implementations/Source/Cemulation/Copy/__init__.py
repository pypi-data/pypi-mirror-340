from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CopyCls:
	"""Copy commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("copy", core, parent)

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	def get_destination(self) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:COPY:DESTination \n
		Snippet: value: int = driver.source.cemulation.copy.get_destination() \n
		No command help available \n
			:return: destination: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:COPY:DESTination?')
		return Conversions.str_to_int(response)

	def set_destination(self, destination: int) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:COPY:DESTination \n
		Snippet: driver.source.cemulation.copy.set_destination(destination = 1) \n
		No command help available \n
			:param destination: No help available
		"""
		param = Conversions.decimal_value_to_str(destination)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:COPY:DESTination {param}')

	def get_source(self) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:COPY:SOURce \n
		Snippet: value: int = driver.source.cemulation.copy.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:COPY:SOURce?')
		return Conversions.str_to_int(response)

	def set_source(self, source: int) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:COPY:SOURce \n
		Snippet: driver.source.cemulation.copy.set_source(source = 1) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.decimal_value_to_str(source)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:COPY:SOURce {param}')

	def clone(self) -> 'CopyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CopyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
