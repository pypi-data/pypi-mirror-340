from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcCls:
	"""Tpc commands group definition. 7 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpc", core, parent)

	@property
	def rdata(self):
		"""rdata commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_rdata'):
			from .Rdata import RdataCls
			self._rdata = RdataCls(self._core, self._cmd_group)
		return self._rdata

	@property
	def sdata(self):
		"""sdata commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_sdata'):
			from .Sdata import SdataCls
			self._sdata = SdataCls(self._core, self._cmd_group)
		return self._sdata

	def clone(self) -> 'TpcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TpcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
