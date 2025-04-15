from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LosCls:
	"""Los commands group definition. 12 total commands, 3 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("los", core, parent)

	@property
	def arrival(self):
		"""arrival commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_arrival'):
			from .Arrival import ArrivalCls
			self._arrival = ArrivalCls(self._core, self._cmd_group)
		return self._arrival

	@property
	def departure(self):
		"""departure commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_departure'):
			from .Departure import DepartureCls
			self._departure = DepartureCls(self._core, self._cmd_group)
		return self._departure

	@property
	def random(self):
		"""random commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_random'):
			from .Random import RandomCls
			self._random = RandomCls(self._core, self._cmd_group)
		return self._random

	def get_distance(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:DISTance \n
		Snippet: value: float = driver.source.cemulation.scm.los.get_distance() \n
		No command help available \n
			:return: los_3_ddistance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:LOS:DISTance?')
		return Conversions.str_to_float(response)

	def set_distance(self, los_3_ddistance: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:DISTance \n
		Snippet: driver.source.cemulation.scm.los.set_distance(los_3_ddistance = 1.0) \n
		No command help available \n
			:param los_3_ddistance: No help available
		"""
		param = Conversions.decimal_value_to_str(los_3_ddistance)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:LOS:DISTance {param}')

	def get_kfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:KFACtor \n
		Snippet: value: float = driver.source.cemulation.scm.los.get_kfactor() \n
		No command help available \n
			:return: factor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:LOS:KFACtor?')
		return Conversions.str_to_float(response)

	def set_kfactor(self, factor: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:KFACtor \n
		Snippet: driver.source.cemulation.scm.los.set_kfactor(factor = 1.0) \n
		No command help available \n
			:param factor: No help available
		"""
		param = Conversions.decimal_value_to_str(factor)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:LOS:KFACtor {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:STATe \n
		Snippet: value: bool = driver.source.cemulation.scm.los.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:LOS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:LOS:STATe \n
		Snippet: driver.source.cemulation.scm.los.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:LOS:STATe {param}')

	def clone(self) -> 'LosCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LosCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
