from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EconfigCls:
	"""Econfig commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("econfig", core, parent)

	@property
	def pconfig(self):
		"""pconfig commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pconfig'):
			from .Pconfig import PconfigCls
			self._pconfig = PconfigCls(self._core, self._cmd_group)
		return self._pconfig

	def clone(self) -> 'EconfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EconfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
