from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BeidouCls:
	"""Beidou commands group definition. 9 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("beidou", core, parent)

	@property
	def svid(self):
		"""svid commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_svid'):
			from .Svid import SvidCls
			self._svid = SvidCls(self._core, self._cmd_group)
		return self._svid

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .Synchronize import SynchronizeCls
			self._synchronize = SynchronizeCls(self._core, self._cmd_group)
		return self._synchronize

	@property
	def toaData(self):
		"""toaData commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_toaData'):
			from .ToaData import ToaDataCls
			self._toaData = ToaDataCls(self._core, self._cmd_group)
		return self._toaData

	def clone(self) -> 'BeidouCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BeidouCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
