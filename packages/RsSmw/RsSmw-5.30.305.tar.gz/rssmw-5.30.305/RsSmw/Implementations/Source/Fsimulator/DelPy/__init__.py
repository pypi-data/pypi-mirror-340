from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelPyCls:
	"""DelPy commands group definition. 24 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delPy", core, parent)

	@property
	def group(self):
		"""group commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_group'):
			from .Group import GroupCls
			self._group = GroupCls(self._core, self._cmd_group)
		return self._group

	@property
	def typePy(self):
		"""typePy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:FSIMulator:DEL:STATe \n
		Snippet: value: bool = driver.source.fsimulator.delPy.get_state() \n
		Enables the fading configurations. Note: Changing the configuration will cause an interruption in the fading process,
		followed by a restart after about one second. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:DEL:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DEL:STATe \n
		Snippet: driver.source.fsimulator.delPy.set_state(state = False) \n
		Enables the fading configurations. Note: Changing the configuration will cause an interruption in the fading process,
		followed by a restart after about one second. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:DEL:STATe {param}')

	def clone(self) -> 'DelPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DelPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
