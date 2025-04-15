from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 8 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	@property
	def aoTime(self):
		"""aoTime commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aoTime'):
			from .AoTime import AoTimeCls
			self._aoTime = AoTimeCls(self._core, self._cmd_group)
		return self._aoTime

	@property
	def hoTime(self):
		"""hoTime commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hoTime'):
			from .HoTime import HoTimeCls
			self._hoTime = HoTimeCls(self._core, self._cmd_group)
		return self._hoTime

	@property
	def sequence(self):
		"""sequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import SequenceCls
			self._sequence = SequenceCls(self._core, self._cmd_group)
		return self._sequence

	@property
	def bb(self):
		"""bb commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
