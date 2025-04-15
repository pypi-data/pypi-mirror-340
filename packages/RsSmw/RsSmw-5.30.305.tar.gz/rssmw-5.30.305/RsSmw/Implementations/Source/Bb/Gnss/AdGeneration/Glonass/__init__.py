from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GlonassCls:
	"""Glonass commands group definition. 10 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("glonass", core, parent)

	@property
	def acquisition(self):
		"""acquisition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acquisition'):
			from .Acquisition import AcquisitionCls
			self._acquisition = AcquisitionCls(self._core, self._cmd_group)
		return self._acquisition

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

	def clone(self) -> 'GlonassCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GlonassCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
