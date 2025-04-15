from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FeatureCls:
	"""Feature commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("feature", core, parent)

	@property
	def snos(self):
		"""snos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snos'):
			from .Snos import SnosCls
			self._snos = SnosCls(self._core, self._cmd_group)
		return self._snos

	def get_activate(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:ACTivate \n
		Snippet: value: str = driver.source.bb.nr5G.feature.get_activate() \n
		No command help available \n
			:return: activat_hidden_fn: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FEATure:ACTivate?')
		return trim_str_response(response)

	def get_deactivate(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:DEACtivate \n
		Snippet: value: str = driver.source.bb.nr5G.feature.get_deactivate() \n
		No command help available \n
			:return: deactivate_feat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FEATure:DEACtivate?')
		return trim_str_response(response)

	def clone(self) -> 'FeatureCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FeatureCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
