from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ProfilingCls:
	"""Profiling commands group definition. 11 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("profiling", core, parent)

	@property
	def hwAccess(self):
		"""hwAccess commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_hwAccess'):
			from .HwAccess import HwAccessCls
			self._hwAccess = HwAccessCls(self._core, self._cmd_group)
		return self._hwAccess

	@property
	def logging(self):
		"""logging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logging'):
			from .Logging import LoggingCls
			self._logging = LoggingCls(self._core, self._cmd_group)
		return self._logging

	@property
	def module(self):
		"""module commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_module'):
			from .Module import ModuleCls
			self._module = ModuleCls(self._core, self._cmd_group)
		return self._module

	@property
	def tick(self):
		"""tick commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tick'):
			from .Tick import TickCls
			self._tick = TickCls(self._core, self._cmd_group)
		return self._tick

	@property
	def tpoint(self):
		"""tpoint commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpoint'):
			from .Tpoint import TpointCls
			self._tpoint = TpointCls(self._core, self._cmd_group)
		return self._tpoint

	def get_state(self) -> bool:
		"""SCPI: SYSTem:PROFiling:STATe \n
		Snippet: value: bool = driver.system.profiling.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SYSTem:PROFiling:STATe \n
		Snippet: driver.system.profiling.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:PROFiling:STATe {param}')

	def clone(self) -> 'ProfilingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ProfilingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
