from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImpairmentCls:
	"""Impairment commands group definition. 34 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("impairment", core, parent)

	@property
	def bbmm(self):
		"""bbmm commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_bbmm'):
			from .Bbmm import BbmmCls
			self._bbmm = BbmmCls(self._core, self._cmd_group)
		return self._bbmm

	@property
	def fader(self):
		"""fader commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_fader'):
			from .Fader import FaderCls
			self._fader = FaderCls(self._core, self._cmd_group)
		return self._fader

	@property
	def iqOutput(self):
		"""iqOutput commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOutput'):
			from .IqOutput import IqOutputCls
			self._iqOutput = IqOutputCls(self._core, self._cmd_group)
		return self._iqOutput

	@property
	def optimization(self):
		"""optimization commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_optimization'):
			from .Optimization import OptimizationCls
			self._optimization = OptimizationCls(self._core, self._cmd_group)
		return self._optimization

	@property
	def rf(self):
		"""rf commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	def clone(self) -> 'ImpairmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImpairmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
