from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StreamCls:
	"""Stream commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stream", core, parent)

	@property
	def buffilled(self):
		"""buffilled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_buffilled'):
			from .Buffilled import BuffilledCls
			self._buffilled = BuffilledCls(self._core, self._cmd_group)
		return self._buffilled

	@property
	def bufRemain(self):
		"""bufRemain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bufRemain'):
			from .BufRemain import BufRemainCls
			self._bufRemain = BufRemainCls(self._core, self._cmd_group)
		return self._bufRemain

	@property
	def drop(self):
		"""drop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_drop'):
			from .Drop import DropCls
			self._drop = DropCls(self._core, self._cmd_group)
		return self._drop

	@property
	def exec(self):
		"""exec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_exec'):
			from .Exec import ExecCls
			self._exec = ExecCls(self._core, self._cmd_group)
		return self._exec

	@property
	def wrdRead(self):
		"""wrdRead commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wrdRead'):
			from .WrdRead import WrdReadCls
			self._wrdRead = WrdReadCls(self._core, self._cmd_group)
		return self._wrdRead

	@property
	def wrdWrite(self):
		"""wrdWrite commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wrdWrite'):
			from .WrdWrite import WrdWriteCls
			self._wrdWrite = WrdWriteCls(self._core, self._cmd_group)
		return self._wrdWrite

	def clone(self) -> 'StreamCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StreamCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
