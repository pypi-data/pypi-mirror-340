from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpsCls:
	"""Tps commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tps", core, parent)

	@property
	def id(self):
		"""id commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def mfec(self):
		"""mfec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mfec'):
			from .Mfec import MfecCls
			self._mfec = MfecCls(self._core, self._cmd_group)
		return self._mfec

	@property
	def tslicing(self):
		"""tslicing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tslicing'):
			from .Tslicing import TslicingCls
			self._tslicing = TslicingCls(self._core, self._cmd_group)
		return self._tslicing

	def clone(self) -> 'TpsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TpsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
