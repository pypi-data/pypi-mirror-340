from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XpuschCls:
	"""Xpusch commands group definition. 13 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xpusch", core, parent)

	@property
	def ccoding(self):
		"""ccoding commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def dmrs(self):
		"""dmrs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def nscid(self):
		"""nscid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nscid'):
			from .Nscid import NscidCls
			self._nscid = NscidCls(self._core, self._cmd_group)
		return self._nscid

	@property
	def pcrs(self):
		"""pcrs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcrs'):
			from .Pcrs import PcrsCls
			self._pcrs = PcrsCls(self._core, self._cmd_group)
		return self._pcrs

	@property
	def precoding(self):
		"""precoding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Precoding import PrecodingCls
			self._precoding = PrecodingCls(self._core, self._cmd_group)
		return self._precoding

	@property
	def rmIndex(self):
		"""rmIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmIndex'):
			from .RmIndex import RmIndexCls
			self._rmIndex = RmIndexCls(self._core, self._cmd_group)
		return self._rmIndex

	def clone(self) -> 'XpuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = XpuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
