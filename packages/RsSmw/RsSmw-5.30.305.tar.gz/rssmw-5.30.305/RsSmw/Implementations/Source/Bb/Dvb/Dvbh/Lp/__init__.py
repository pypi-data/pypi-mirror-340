from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LpCls:
	"""Lp commands group definition. 7 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lp", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def icoder(self):
		"""icoder commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_icoder'):
			from .Icoder import IcoderCls
			self._icoder = IcoderCls(self._core, self._cmd_group)
		return self._icoder

	@property
	def ocoder(self):
		"""ocoder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ocoder'):
			from .Ocoder import OcoderCls
			self._ocoder = OcoderCls(self._core, self._cmd_group)
		return self._ocoder

	@property
	def ointerleaver(self):
		"""ointerleaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ointerleaver'):
			from .Ointerleaver import OinterleaverCls
			self._ointerleaver = OinterleaverCls(self._core, self._cmd_group)
		return self._ointerleaver

	@property
	def pnScrambler(self):
		"""pnScrambler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnScrambler'):
			from .PnScrambler import PnScramblerCls
			self._pnScrambler = PnScramblerCls(self._core, self._cmd_group)
		return self._pnScrambler

	def clone(self) -> 'LpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
