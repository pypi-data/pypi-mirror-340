from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MdelayCls:
	"""Mdelay commands group definition. 23 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mdelay", core, parent)

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def del30(self):
		"""del30 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_del30'):
			from .Del30 import Del30Cls
			self._del30 = Del30Cls(self._core, self._cmd_group)
		return self._del30

	@property
	def moving(self):
		"""moving commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_moving'):
			from .Moving import MovingCls
			self._moving = MovingCls(self._core, self._cmd_group)
		return self._moving

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:STATe \n
		Snippet: value: bool = driver.source.cemulation.mdelay.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:STATe \n
		Snippet: driver.source.cemulation.mdelay.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:STATe {param}')

	def clone(self) -> 'MdelayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MdelayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
