from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhaseCls:
	"""Phase commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phase", core, parent)

	@property
	def hh(self):
		"""hh commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hh'):
			from .Hh import HhCls
			self._hh = HhCls(self._core, self._cmd_group)
		return self._hh

	@property
	def hv(self):
		"""hv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hv'):
			from .Hv import HvCls
			self._hv = HvCls(self._core, self._cmd_group)
		return self._hv

	@property
	def vh(self):
		"""vh commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vh'):
			from .Vh import VhCls
			self._vh = VhCls(self._core, self._cmd_group)
		return self._vh

	@property
	def vv(self):
		"""vv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vv'):
			from .Vv import VvCls
			self._vv = VvCls(self._core, self._cmd_group)
		return self._vv

	def clone(self) -> 'PhaseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PhaseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
