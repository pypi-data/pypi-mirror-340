from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClockCls:
	"""Clock commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("clock", core, parent)

	@property
	def af(self):
		"""af commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_af'):
			from .Af import AfCls
			self._af = AfCls(self._core, self._cmd_group)
		return self._af

	@property
	def tgd(self):
		"""tgd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgd'):
			from .Tgd import TgdCls
			self._tgd = TgdCls(self._core, self._cmd_group)
		return self._tgd

	@property
	def toc(self):
		"""toc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toc'):
			from .Toc import TocCls
			self._toc = TocCls(self._core, self._cmd_group)
		return self._toc

	@property
	def wnoc(self):
		"""wnoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnoc'):
			from .Wnoc import WnocCls
			self._wnoc = WnocCls(self._core, self._cmd_group)
		return self._wnoc

	def clone(self) -> 'ClockCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ClockCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
