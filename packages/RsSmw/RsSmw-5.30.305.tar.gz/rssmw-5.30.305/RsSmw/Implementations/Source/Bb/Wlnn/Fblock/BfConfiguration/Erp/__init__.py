from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ErpCls:
	"""Erp commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("erp", core, parent)

	@property
	def bpMode(self):
		"""bpMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpMode'):
			from .BpMode import BpModeCls
			self._bpMode = BpModeCls(self._core, self._cmd_group)
		return self._bpMode

	@property
	def nePresent(self):
		"""nePresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nePresent'):
			from .NePresent import NePresentCls
			self._nePresent = NePresentCls(self._core, self._cmd_group)
		return self._nePresent

	@property
	def uprotection(self):
		"""uprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uprotection'):
			from .Uprotection import UprotectionCls
			self._uprotection = UprotectionCls(self._core, self._cmd_group)
		return self._uprotection

	def clone(self) -> 'ErpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ErpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
