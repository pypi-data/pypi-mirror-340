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
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:FRATio \n
		Snippet: value: float = driver.source.fsimulator.tcInterferer.moving.get_fratio() \n
		Sets the ratio of the actual Doppler frequency to the set Doppler frequency for the reference and moving path with 2
		channel interferer fading. \n
			:return: fratio: float Range: -1 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:FRATio?')
		return Conversions.str_to_float(response)

	def set_fratio(self, fratio: float) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:FRATio \n
		Snippet: driver.source.fsimulator.tcInterferer.moving.set_fratio(fratio = 1.0) \n
		Sets the ratio of the actual Doppler frequency to the set Doppler frequency for the reference and moving path with 2
		channel interferer fading. \n
			:param fratio: float Range: -1 to 1
		"""
		param = Conversions.decimal_value_to_str(fratio)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:FRATio {param}')

	def get_loss(self) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:LOSS \n
		Snippet: value: float = driver.source.fsimulator.tcInterferer.moving.get_loss() \n
		Seta the loss of the reference and moving path with 2 channel interferer fading. \n
			:return: loss: float Range: 0 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, loss: float) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:LOSS \n
		Snippet: driver.source.fsimulator.tcInterferer.moving.set_loss(loss = 1.0) \n
		Seta the loss of the reference and moving path with 2 channel interferer fading. \n
			:param loss: float Range: 0 to 50
		"""
		param = Conversions.decimal_value_to_str(loss)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:LOSS {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.Fad2CitfMode:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:MMODe \n
		Snippet: value: enums.Fad2CitfMode = driver.source.fsimulator.tcInterferer.moving.get_mmode() \n
		Selects the type of moving applied to the moving path. \n
			:return: mmode: SLIDing| HOPPing
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.Fad2CitfMode)

	def set_mmode(self, mmode: enums.Fad2CitfMode) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:MMODe \n
		Snippet: driver.source.fsimulator.tcInterferer.moving.set_mmode(mmode = enums.Fad2CitfMode.HOPPing) \n
		Selects the type of moving applied to the moving path. \n
			:param mmode: SLIDing| HOPPing
		"""
		param = Conversions.enum_scalar_to_str(mmode, enums.Fad2CitfMode)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:MMODe {param}')

	# noinspection PyTypeChecker
	def get_profile(self) -> enums.FadingProfileB:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:PROFile \n
		Snippet: value: enums.FadingProfileB = driver.source.fsimulator.tcInterferer.moving.get_profile() \n
		Sets the fading profile to be used for the reference and moving path with 2 channel interferer fading. \n
			:return: profile: SPATh| PDOPpler| RAYLeigh
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:PROFile?')
		return Conversions.str_to_scalar_enum(response, enums.FadingProfileB)

	def set_profile(self, profile: enums.FadingProfileB) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:PROFile \n
		Snippet: driver.source.fsimulator.tcInterferer.moving.set_profile(profile = enums.FadingProfileB.BELLindoor) \n
		Sets the fading profile to be used for the reference and moving path with 2 channel interferer fading. \n
			:param profile: SPATh| PDOPpler| RAYLeigh
		"""
		param = Conversions.enum_scalar_to_str(profile, enums.FadingProfileB)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:PROFile {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:STATe \n
		Snippet: value: bool = driver.source.fsimulator.tcInterferer.moving.get_state() \n
		Activate the reference and moving path of the 2 channel interferer fading configuration. The 2 channel interferer fading
		configuration and the fading simulator must be switched on separately, see [:SOURce<hw>]:FSIMulator:TCINterferer[:STATe]
		and .[:SOURce<hw>]:FSIMulator[:STATe] \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:TCINterferer:MOVing:STATe \n
		Snippet: driver.source.fsimulator.tcInterferer.moving.set_state(state = False) \n
		Activate the reference and moving path of the 2 channel interferer fading configuration. The 2 channel interferer fading
		configuration and the fading simulator must be switched on separately, see [:SOURce<hw>]:FSIMulator:TCINterferer[:STATe]
		and .[:SOURce<hw>]:FSIMulator[:STATe] \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:TCINterferer:MOVing:STATe {param}')

	def clone(self) -> 'MovingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MovingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
