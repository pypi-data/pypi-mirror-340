from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 11 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def band(self):
		"""band commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_band'):
			from .Band import BandCls
			self._band = BandCls(self._core, self._cmd_group)
		return self._band

	@property
	def bconfig(self):
		"""bconfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bconfig'):
			from .Bconfig import BconfigCls
			self._bconfig = BconfigCls(self._core, self._cmd_group)
		return self._bconfig

	@property
	def ifrequency(self):
		"""ifrequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ifrequency'):
			from .Ifrequency import IfrequencyCls
			self._ifrequency = IfrequencyCls(self._core, self._cmd_group)
		return self._ifrequency

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	def clone(self) -> 'FrequencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrequencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
