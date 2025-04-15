from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	@property
	def auser(self):
		"""auser commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auser'):
			from .Auser import AuserCls
			self._auser = AuserCls(self._core, self._cmd_group)
		return self._auser

	@property
	def feedback(self):
		"""feedback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_feedback'):
			from .Feedback import FeedbackCls
			self._feedback = FeedbackCls(self._core, self._cmd_group)
		return self._feedback

	def clone(self) -> 'DelayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DelayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
