from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DohertyCls:
	"""Doherty commands group definition. 47 total commands, 11 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("doherty", core, parent)

	@property
	def amam(self):
		"""amam commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amam'):
			from .Amam import AmamCls
			self._amam = AmamCls(self._core, self._cmd_group)
		return self._amam

	@property
	def amPm(self):
		"""amPm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amPm'):
			from .AmPm import AmPmCls
			self._amPm = AmPmCls(self._core, self._cmd_group)
		return self._amPm

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def lrf(self):
		"""lrf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lrf'):
			from .Lrf import LrfCls
			self._lrf = LrfCls(self._core, self._cmd_group)
		return self._lrf

	@property
	def measurement(self):
		"""measurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measurement'):
			from .Measurement import MeasurementCls
			self._measurement = MeasurementCls(self._core, self._cmd_group)
		return self._measurement

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pin'):
			from .Pin import PinCls
			self._pin = PinCls(self._core, self._cmd_group)
		return self._pin

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def shaping(self):
		"""shaping commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_shaping'):
			from .Shaping import ShapingCls
			self._shaping = ShapingCls(self._core, self._cmd_group)
		return self._shaping

	# noinspection PyTypeChecker
	def get_scale(self) -> enums.IqOutEnvScale:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SCALe \n
		Snippet: value: enums.IqOutEnvScale = driver.source.iq.doherty.get_scale() \n
		Determines the units used on the x and y-axis. \n
			:return: scale: POWer| VOLTage
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvScale)

	def set_scale(self, scale: enums.IqOutEnvScale) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SCALe \n
		Snippet: driver.source.iq.doherty.set_scale(scale = enums.IqOutEnvScale.POWer) \n
		Determines the units used on the x and y-axis. \n
			:param scale: POWer| VOLTage
		"""
		param = Conversions.enum_scalar_to_str(scale, enums.IqOutEnvScale)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SCALe {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:IQ:DOHerty:STATe \n
		Snippet: value: bool = driver.source.iq.doherty.get_state() \n
		Enabels/disables the generation of digitally Doherty signals. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce:IQ:DOHerty:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce]:IQ:DOHerty:STATe \n
		Snippet: driver.source.iq.doherty.set_state(state = False) \n
		Enabels/disables the generation of digitally Doherty signals. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:IQ:DOHerty:STATe {param}')

	def clone(self) -> 'DohertyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DohertyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
