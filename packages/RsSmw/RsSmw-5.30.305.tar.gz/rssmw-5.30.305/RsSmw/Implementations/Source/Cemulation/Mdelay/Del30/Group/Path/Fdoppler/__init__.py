from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdopplerCls:
	"""Fdoppler commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdoppler", core, parent)

	@property
	def actual(self):
		"""actual commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_actual'):
			from .Actual import ActualCls
			self._actual = ActualCls(self._core, self._cmd_group)
		return self._actual

	def set(self, fdoppler: float, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:DEL30:GROup<ST>:PATH<CH>:FDOPpler \n
		Snippet: driver.source.cemulation.mdelay.del30.group.path.fdoppler.set(fdoppler = 1.0, fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param fdoppler: No help available
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.decimal_value_to_str(fdoppler)
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:DEL30:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:FDOPpler {param}')

	def get(self, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:DEL30:GROup<ST>:PATH<CH>:FDOPpler \n
		Snippet: value: float = driver.source.cemulation.mdelay.del30.group.path.fdoppler.get(fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: fdoppler: No help available"""
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MDELay:DEL30:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:FDOPpler?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FdopplerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FdopplerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
