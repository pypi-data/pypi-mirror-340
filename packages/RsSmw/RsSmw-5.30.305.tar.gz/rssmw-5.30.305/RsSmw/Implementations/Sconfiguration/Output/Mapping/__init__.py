from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MappingCls:
	"""Mapping commands group definition. 12 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mapping", core, parent)

	@property
	def bbmm(self):
		"""bbmm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bbmm'):
			from .Bbmm import BbmmCls
			self._bbmm = BbmmCls(self._core, self._cmd_group)
		return self._bbmm

	@property
	def fader(self):
		"""fader commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fader'):
			from .Fader import FaderCls
			self._fader = FaderCls(self._core, self._cmd_group)
		return self._fader

	@property
	def iqOutput(self):
		"""iqOutput commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOutput'):
			from .IqOutput import IqOutputCls
			self._iqOutput = IqOutputCls(self._core, self._cmd_group)
		return self._iqOutput

	@property
	def rf(self):
		"""rf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	@property
	def stream(self):
		"""stream commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Stream import StreamCls
			self._stream = StreamCls(self._core, self._cmd_group)
		return self._stream

	def clone(self) -> 'MappingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MappingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
