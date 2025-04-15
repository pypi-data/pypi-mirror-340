from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TgnCls:
	"""Tgn commands group definition. 7 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tgn", core, parent)

	@property
	def distribution(self):
		"""distribution commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_distribution'):
			from .Distribution import DistributionCls
			self._distribution = DistributionCls(self._core, self._cmd_group)
		return self._distribution

	@property
	def ray(self):
		"""ray commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ray'):
			from .Ray import RayCls
			self._ray = RayCls(self._core, self._cmd_group)
		return self._ray

	def clone(self) -> 'TgnCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TgnCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
