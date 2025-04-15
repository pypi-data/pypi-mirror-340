from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BirthDeathCls:
	"""BirthDeath commands group definition. 13 total commands, 3 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("birthDeath", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def hopping(self):
		"""hopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopping'):
			from .Hopping import HoppingCls
			self._hopping = HoppingCls(self._core, self._cmd_group)
		return self._hopping

	@property
	def path(self):
		"""path commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	def get_fratio(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:FRATio \n
		Snippet: value: float = driver.source.cemulation.birthDeath.get_fratio() \n
		No command help available \n
			:return: fratio: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:FRATio?')
		return Conversions.str_to_float(response)

	def set_fratio(self, fratio: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:FRATio \n
		Snippet: driver.source.cemulation.birthDeath.set_fratio(fratio = 1.0) \n
		No command help available \n
			:param fratio: No help available
		"""
		param = Conversions.decimal_value_to_str(fratio)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:FRATio {param}')

	def get_positions(self) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:POSitions \n
		Snippet: value: int = driver.source.cemulation.birthDeath.get_positions() \n
		No command help available \n
			:return: positions: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:POSitions?')
		return Conversions.str_to_int(response)

	def set_positions(self, positions: int) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:POSitions \n
		Snippet: driver.source.cemulation.birthDeath.set_positions(positions = 1) \n
		No command help available \n
			:param positions: No help available
		"""
		param = Conversions.decimal_value_to_str(positions)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:POSitions {param}')

	def get_soffset(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:SOFFset \n
		Snippet: value: float = driver.source.cemulation.birthDeath.get_soffset() \n
		No command help available \n
			:return: soffset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:SOFFset?')
		return Conversions.str_to_float(response)

	def set_soffset(self, soffset: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:SOFFset \n
		Snippet: driver.source.cemulation.birthDeath.set_soffset(soffset = 1.0) \n
		No command help available \n
			:param soffset: No help available
		"""
		param = Conversions.decimal_value_to_str(soffset)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:SOFFset {param}')

	def get_speed(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:SPEed \n
		Snippet: value: float = driver.source.cemulation.birthDeath.get_speed() \n
		No command help available \n
			:return: speed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:SPEed?')
		return Conversions.str_to_float(response)

	def set_speed(self, speed: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:SPEed \n
		Snippet: driver.source.cemulation.birthDeath.set_speed(speed = 1.0) \n
		No command help available \n
			:param speed: No help available
		"""
		param = Conversions.decimal_value_to_str(speed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:SPEed {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:STATe \n
		Snippet: value: bool = driver.source.cemulation.birthDeath.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:BIRThdeath:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:BIRThdeath:STATe \n
		Snippet: driver.source.cemulation.birthDeath.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:BIRThdeath:STATe {param}')

	def clone(self) -> 'BirthDeathCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BirthDeathCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
