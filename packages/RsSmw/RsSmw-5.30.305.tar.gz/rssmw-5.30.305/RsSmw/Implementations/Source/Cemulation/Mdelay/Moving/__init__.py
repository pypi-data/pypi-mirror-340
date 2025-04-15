from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MovingCls:
	"""Moving commands group definition. 5 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("moving", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:LOSS \n
		Snippet: value: float = driver.source.cemulation.mdelay.moving.get_loss() \n
		No command help available \n
			:return: loss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:MOVing:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:LOSS \n
		Snippet: driver.source.cemulation.mdelay.moving.set_loss(loss = 1.0) \n
		No command help available \n
			:param loss: No help available
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:MOVing:LOSS {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:STATe \n
		Snippet: value: bool = driver.source.cemulation.mdelay.moving.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:MOVing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:STATe \n
		Snippet: driver.source.cemulation.mdelay.moving.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:MOVing:STATe {param}')

	def get_vperiod(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:VPERiod \n
		Snippet: value: float = driver.source.cemulation.mdelay.moving.get_vperiod() \n
		No command help available \n
			:return: vperiod: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:MOVing:VPERiod?')
		return Conversions.str_to_float(response)

	def set_vperiod(self, vperiod: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:MOVing:VPERiod \n
		Snippet: driver.source.cemulation.mdelay.moving.set_vperiod(vperiod = 1.0) \n
		No command help available \n
			:param vperiod: No help available
		"""
		param = Conversions.decimal_value_to_str(vperiod)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:MOVing:VPERiod {param}')

	def clone(self) -> 'MovingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MovingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
