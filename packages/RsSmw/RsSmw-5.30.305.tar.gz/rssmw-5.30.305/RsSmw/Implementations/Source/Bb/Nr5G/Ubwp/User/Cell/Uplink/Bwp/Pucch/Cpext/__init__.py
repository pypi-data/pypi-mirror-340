from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpextCls:
	"""Cpext commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cpext", core, parent)

	@property
	def ncpxt(self):
		"""ncpxt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncpxt'):
			from .Ncpxt import NcpxtCls
			self._ncpxt = NcpxtCls(self._core, self._cmd_group)
		return self._ncpxt

	@property
	def val(self):
		"""val commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_val'):
			from .Val import ValCls
			self._val = ValCls(self._core, self._cmd_group)
		return self._val

	def clone(self) -> 'CpextCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CpextCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
