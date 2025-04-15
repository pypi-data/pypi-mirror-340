from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 7 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def nmessage(self):
		"""nmessage commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Nmessage import NmessageCls
			self._nmessage = NmessageCls(self._core, self._cmd_group)
		return self._nmessage

	@property
	def pcode(self):
		"""pcode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcode'):
			from .Pcode import PcodeCls
			self._pcode = PcodeCls(self._core, self._cmd_group)
		return self._pcode

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	def clone(self) -> 'DataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
