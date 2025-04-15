from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LosCls:
	"""Los commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("los", core, parent)

	@property
	def aazimuth(self):
		"""aazimuth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aazimuth'):
			from .Aazimuth import AazimuthCls
			self._aazimuth = AazimuthCls(self._core, self._cmd_group)
		return self._aazimuth

	@property
	def aelevation(self):
		"""aelevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aelevation'):
			from .Aelevation import AelevationCls
			self._aelevation = AelevationCls(self._core, self._cmd_group)
		return self._aelevation

	@property
	def cpDrift(self):
		"""cpDrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpDrift'):
			from .CpDrift import CpDriftCls
			self._cpDrift = CpDriftCls(self._core, self._cmd_group)
		return self._cpDrift

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Cphase import CphaseCls
			self._cphase = CphaseCls(self._core, self._cmd_group)
		return self._cphase

	@property
	def dshift(self):
		"""dshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dshift'):
			from .Dshift import DshiftCls
			self._dshift = DshiftCls(self._core, self._cmd_group)
		return self._dshift

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import EnableCls
			self._enable = EnableCls(self._core, self._cmd_group)
		return self._enable

	@property
	def icPhase(self):
		"""icPhase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icPhase'):
			from .IcPhase import IcPhaseCls
			self._icPhase = IcPhaseCls(self._core, self._cmd_group)
		return self._icPhase

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	def clone(self) -> 'LosCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LosCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
