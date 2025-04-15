from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApaichCls:
	"""Apaich commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apaich", core, parent)

	@property
	def aslot(self):
		"""aslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aslot'):
			from .Aslot import AslotCls
			self._aslot = AslotCls(self._core, self._cmd_group)
		return self._aslot

	@property
	def saPattern(self):
		"""saPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saPattern'):
			from .SaPattern import SaPatternCls
			self._saPattern = SaPatternCls(self._core, self._cmd_group)
		return self._saPattern

	def clone(self) -> 'ApaichCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApaichCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
