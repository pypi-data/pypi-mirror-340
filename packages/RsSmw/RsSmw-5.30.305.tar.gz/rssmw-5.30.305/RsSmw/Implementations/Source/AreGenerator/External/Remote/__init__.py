from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoteCls:
	"""Remote commands group definition. 8 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remote", core, parent)

	@property
	def edit(self):
		"""edit commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_edit'):
			from .Edit import EditCls
			self._edit = EditCls(self._core, self._cmd_group)
		return self._edit

	def clone(self) -> 'RemoteCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RemoteCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
