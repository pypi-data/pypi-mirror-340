from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CombinedCls:
	"""Combined commands group definition. 6 total commands, 1 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("combined", core, parent)

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	def get_count(self) -> int:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:COUNt \n
		Snippet: value: int = driver.source.sweep.combined.get_count() \n
		No command help available \n
			:return: step_count: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:COMBined:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, step_count: int) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:COUNt \n
		Snippet: driver.source.sweep.combined.set_count(step_count = 1) \n
		No command help available \n
			:param step_count: No help available
		"""
		param = Conversions.decimal_value_to_str(step_count)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:COUNt {param}')

	def get_dwell(self) -> float:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:DWELl \n
		Snippet: value: float = driver.source.sweep.combined.get_dwell() \n
		No command help available \n
			:return: dwell: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:COMBined:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:DWELl \n
		Snippet: driver.source.sweep.combined.set_dwell(dwell = 1.0) \n
		No command help available \n
			:param dwell: No help available
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:DWELl {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AutoManStep:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:MODE \n
		Snippet: value: enums.AutoManStep = driver.source.sweep.combined.get_mode() \n
		No command help available \n
			:return: sweep_comb_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:COMBined:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManStep)

	def set_mode(self, sweep_comb_mode: enums.AutoManStep) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:MODE \n
		Snippet: driver.source.sweep.combined.set_mode(sweep_comb_mode = enums.AutoManStep.AUTO) \n
		No command help available \n
			:param sweep_comb_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(sweep_comb_mode, enums.AutoManStep)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:MODE {param}')

	def get_retrace(self) -> bool:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:RETRace \n
		Snippet: value: bool = driver.source.sweep.combined.get_retrace() \n
		No command help available \n
			:return: retrace_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:COMBined:RETRace?')
		return Conversions.str_to_bool(response)

	def set_retrace(self, retrace_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:RETRace \n
		Snippet: driver.source.sweep.combined.set_retrace(retrace_state = False) \n
		No command help available \n
			:param retrace_state: No help available
		"""
		param = Conversions.bool_to_str(retrace_state)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:RETRace {param}')

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.SweCyclMode:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:SHAPe \n
		Snippet: value: enums.SweCyclMode = driver.source.sweep.combined.get_shape() \n
		No command help available \n
			:return: shape: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:COMBined:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.SweCyclMode)

	def set_shape(self, shape: enums.SweCyclMode) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:SHAPe \n
		Snippet: driver.source.sweep.combined.set_shape(shape = enums.SweCyclMode.SAWTooth) \n
		No command help available \n
			:param shape: No help available
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.SweCyclMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:SHAPe {param}')

	def clone(self) -> 'CombinedCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CombinedCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
