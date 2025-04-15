from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L2BandCls:
	"""L2Band commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l2Band", core, parent)

	@property
	def ca(self):
		"""ca commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ca'):
			from .Ca import CaCls
			self._ca = CaCls(self._core, self._cmd_group)
		return self._ca

	@property
	def l2C(self):
		"""l2C commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l2C'):
			from .L2C import L2CCls
			self._l2C = L2CCls(self._core, self._cmd_group)
		return self._l2C

	@property
	def m(self):
		"""m commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_m'):
			from .M import MCls
			self._m = MCls(self._core, self._cmd_group)
		return self._m

	@property
	def p(self):
		"""p commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_p'):
			from .P import PCls
			self._p = PCls(self._core, self._cmd_group)
		return self._p

	@property
	def py(self):
		"""py commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_py'):
			from .Py import PyCls
			self._py = PyCls(self._core, self._cmd_group)
		return self._py

	def clone(self) -> 'L2BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L2BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
