from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScmaCls:
	"""Scma commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scma", core, parent)

	@property
	def codebook(self):
		"""codebook commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codebook'):
			from .Codebook import CodebookCls
			self._codebook = CodebookCls(self._core, self._cmd_group)
		return self._codebook

	@property
	def layer(self):
		"""layer commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_layer'):
			from .Layer import LayerCls
			self._layer = LayerCls(self._core, self._cmd_group)
		return self._layer

	@property
	def nlayers(self):
		"""nlayers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nlayers'):
			from .Nlayers import NlayersCls
			self._nlayers = NlayersCls(self._core, self._cmd_group)
		return self._nlayers

	@property
	def spread(self):
		"""spread commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spread'):
			from .Spread import SpreadCls
			self._spread = SpreadCls(self._core, self._cmd_group)
		return self._spread

	def clone(self) -> 'ScmaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScmaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
