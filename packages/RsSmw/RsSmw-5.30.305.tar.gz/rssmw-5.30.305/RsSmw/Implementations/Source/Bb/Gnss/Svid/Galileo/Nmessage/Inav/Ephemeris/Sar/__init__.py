from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SarCls:
	"""Sar commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sar", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def rlm(self):
		"""rlm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlm'):
			from .Rlm import RlmCls
			self._rlm = RlmCls(self._core, self._cmd_group)
		return self._rlm

	@property
	def spare(self):
		"""spare commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spare'):
			from .Spare import SpareCls
			self._spare = SpareCls(self._core, self._cmd_group)
		return self._spare

	def clone(self) -> 'SarCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SarCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
