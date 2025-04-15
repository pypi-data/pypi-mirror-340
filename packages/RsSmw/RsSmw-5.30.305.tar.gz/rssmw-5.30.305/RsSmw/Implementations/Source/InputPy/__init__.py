from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 20 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	@property
	def modext(self):
		"""modext commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_modext'):
			from .Modext import ModextCls
			self._modext = ModextCls(self._core, self._cmd_group)
		return self._modext

	@property
	def tm(self):
		"""tm commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tm'):
			from .Tm import TmCls
			self._tm = TmCls(self._core, self._cmd_group)
		return self._tm

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def user(self):
		"""user commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'InputPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
