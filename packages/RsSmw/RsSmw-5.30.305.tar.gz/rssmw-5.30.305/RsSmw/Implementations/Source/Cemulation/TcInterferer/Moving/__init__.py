from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MovingCls:
	"""Moving commands group definition. 9 total commands, 2 Subgroups, 5 group commands"""

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

	@property
	def fdoppler(self):
		"""fdoppler commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdoppler'):
			from .Fdoppler import FdopplerCls
			self._fdoppler = FdopplerCls(self._core, self._cmd_group)
		return self._fdoppler

	def get_fratio(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:FRATio \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.get_fratio() \n
		No command help available \n
			:return: fratio: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:FRATio?')
		return Conversions.str_to_float(response)

	def set_fratio(self, fratio: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:FRATio \n
		Snippet: driver.source.cemulation.tcInterferer.moving.set_fratio(fratio = 1.0) \n
		No command help available \n
			:param fratio: No help available
		"""
		param = Conversions.decimal_value_to_str(fratio)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:FRATio {param}')

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:LOSS \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.get_loss() \n
		No command help available \n
			:return: loss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:LOSS \n
		Snippet: driver.source.cemulation.tcInterferer.moving.set_loss(loss = 1.0) \n
		No command help available \n
			:param loss: No help available
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:LOSS {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.Fad2CitfMode:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:MMODe \n
		Snippet: value: enums.Fad2CitfMode = driver.source.cemulation.tcInterferer.moving.get_mmode() \n
		No command help available \n
			:return: mmode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.Fad2CitfMode)

	def set_mmode(self, mmode: enums.Fad2CitfMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:MMODe \n
		Snippet: driver.source.cemulation.tcInterferer.moving.set_mmode(mmode = enums.Fad2CitfMode.HOPPing) \n
		No command help available \n
			:param mmode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mmode, enums.Fad2CitfMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:MMODe {param}')

	# noinspection PyTypeChecker
	def get_profile(self) -> enums.FadingProfileB:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:PROFile \n
		Snippet: value: enums.FadingProfileB = driver.source.cemulation.tcInterferer.moving.get_profile() \n
		No command help available \n
			:return: profile: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:PROFile?')
		return Conversions.str_to_scalar_enum(response, enums.FadingProfileB)

	def set_profile(self, profile: enums.FadingProfileB) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:PROFile \n
		Snippet: driver.source.cemulation.tcInterferer.moving.set_profile(profile = enums.FadingProfileB.BELLindoor) \n
		No command help available \n
			:param profile: No help available
		"""
		param = Conversions.enum_scalar_to_str(profile, enums.FadingProfileB)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:PROFile {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:STATe \n
		Snippet: value: bool = driver.source.cemulation.tcInterferer.moving.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:STATe \n
		Snippet: driver.source.cemulation.tcInterferer.moving.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:STATe {param}')

	def clone(self) -> 'MovingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MovingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
