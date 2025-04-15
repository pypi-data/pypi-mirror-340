from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrelationCls:
	"""Correlation commands group definition. 234 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correlation", core, parent)

	@property
	def diagnostic(self):
		"""diagnostic commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_diagnostic'):
			from .Diagnostic import DiagnosticCls
			self._diagnostic = DiagnosticCls(self._core, self._cmd_group)
		return self._diagnostic

	@property
	def rx(self):
		"""rx commands group. 29 Sub-classes, 0 commands."""
		if not hasattr(self, '_rx'):
			from .Rx import RxCls
			self._rx = RxCls(self._core, self._cmd_group)
		return self._rx

	@property
	def tx(self):
		"""tx commands group. 29 Sub-classes, 0 commands."""
		if not hasattr(self, '_tx'):
			from .Tx import TxCls
			self._tx = TxCls(self._core, self._cmd_group)
		return self._tx

	def clone(self) -> 'CorrelationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CorrelationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
