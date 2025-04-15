from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RcsCls:
	"""Rcs commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rcs", core, parent)

	@property
	def mean(self):
		"""mean commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mean'):
			from .Mean import MeanCls
			self._mean = MeanCls(self._core, self._cmd_group)
		return self._mean

	@property
	def model(self):
		"""model commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_model'):
			from .Model import ModelCls
			self._model = ModelCls(self._core, self._cmd_group)
		return self._model

	@property
	def peak(self):
		"""peak commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_peak'):
			from .Peak import PeakCls
			self._peak = PeakCls(self._core, self._cmd_group)
		return self._peak

	@property
	def sper(self):
		"""sper commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sper'):
			from .Sper import SperCls
			self._sper = SperCls(self._core, self._cmd_group)
		return self._sper

	@property
	def tcoverage(self):
		"""tcoverage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcoverage'):
			from .Tcoverage import TcoverageCls
			self._tcoverage = TcoverageCls(self._core, self._cmd_group)
		return self._tcoverage

	@property
	def upInterval(self):
		"""upInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_upInterval'):
			from .UpInterval import UpIntervalCls
			self._upInterval = UpIntervalCls(self._core, self._cmd_group)
		return self._upInterval

	def clone(self) -> 'RcsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RcsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
