from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TcInterfererCls:
	"""TcInterferer commands group definition. 21 total commands, 2 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tcInterferer", core, parent)

	@property
	def moving(self):
		"""moving commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_moving'):
			from .Moving import MovingCls
			self._moving = MovingCls(self._core, self._cmd_group)
		return self._moving

	@property
	def reference(self):
		"""reference commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:PERiod \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.get_period() \n
		No command help available \n
			:return: period: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:PERiod \n
		Snippet: driver.source.cemulation.tcInterferer.set_period(period = 1.0) \n
		No command help available \n
			:param period: No help available
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:PERiod {param}')

	def get_speed(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:SPEed \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.get_speed() \n
		No command help available \n
			:return: speed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:SPEed?')
		return Conversions.str_to_float(response)

	def set_speed(self, speed: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:SPEed \n
		Snippet: driver.source.cemulation.tcInterferer.set_speed(speed = 1.0) \n
		No command help available \n
			:param speed: No help available
		"""
		param = Conversions.decimal_value_to_str(speed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:SPEed {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:[STATe] \n
		Snippet: value: bool = driver.source.cemulation.tcInterferer.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:[STATe] \n
		Snippet: driver.source.cemulation.tcInterferer.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:STATe {param}')

	def clone(self) -> 'TcInterfererCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TcInterfererCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
