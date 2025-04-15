from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SgDefinitionCls:
	"""SgDefinition commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sgDefinition", core, parent)

	@property
	def a(self):
		"""a commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_a'):
			from .A import ACls
			self._a = ACls(self._core, self._cmd_group)
		return self._a

	@property
	def b(self):
		"""b commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_b'):
			from .B import BCls
			self._b = BCls(self._core, self._cmd_group)
		return self._b

	@property
	def c(self):
		"""c commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_c'):
			from .C import CCls
			self._c = CCls(self._core, self._cmd_group)
		return self._c

	@property
	def d(self):
		"""d commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_d'):
			from .D import DCls
			self._d = DCls(self._core, self._cmd_group)
		return self._d

	@property
	def e(self):
		"""e commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_e'):
			from .E import ECls
			self._e = ECls(self._core, self._cmd_group)
		return self._e

	@property
	def f(self):
		"""f commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_f'):
			from .F import FCls
			self._f = FCls(self._core, self._cmd_group)
		return self._f

	@property
	def g(self):
		"""g commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_g'):
			from .G import GCls
			self._g = GCls(self._core, self._cmd_group)
		return self._g

	@property
	def h(self):
		"""h commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_h'):
			from .H import HCls
			self._h = HCls(self._core, self._cmd_group)
		return self._h

	def clone(self) -> 'SgDefinitionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SgDefinitionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
