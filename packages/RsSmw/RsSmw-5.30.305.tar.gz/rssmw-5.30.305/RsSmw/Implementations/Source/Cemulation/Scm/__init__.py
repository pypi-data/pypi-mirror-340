from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScmCls:
	"""Scm commands group definition. 53 total commands, 5 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scm", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .Antenna import AntennaCls
			self._antenna = AntennaCls(self._core, self._cmd_group)
		return self._antenna

	@property
	def d3Mode(self):
		"""d3Mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_d3Mode'):
			from .D3Mode import D3ModeCls
			self._d3Mode = D3ModeCls(self._core, self._cmd_group)
		return self._d3Mode

	@property
	def los(self):
		"""los commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_los'):
			from .Los import LosCls
			self._los = LosCls(self._core, self._cmd_group)
		return self._los

	@property
	def polarization(self):
		"""polarization commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_polarization'):
			from .Polarization import PolarizationCls
			self._polarization = PolarizationCls(self._core, self._cmd_group)
		return self._polarization

	@property
	def tap(self):
		"""tap commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tap'):
			from .Tap import TapCls
			self._tap = TapCls(self._core, self._cmd_group)
		return self._tap

	def get_dot(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:DOT \n
		Snippet: value: float = driver.source.cemulation.scm.get_dot() \n
		No command help available \n
			:return: dir_of_travel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dir_of_travel: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:DOT \n
		Snippet: driver.source.cemulation.scm.set_dot(dir_of_travel = 1.0) \n
		No command help available \n
			:param dir_of_travel: No help available
		"""
		param = Conversions.decimal_value_to_str(dir_of_travel)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:DOT {param}')

	def get_phi(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:PHI \n
		Snippet: value: float = driver.source.cemulation.scm.get_phi() \n
		No command help available \n
			:return: scm_phi: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:PHI?')
		return Conversions.str_to_float(response)

	def set_phi(self, scm_phi: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:PHI \n
		Snippet: driver.source.cemulation.scm.set_phi(scm_phi = 1.0) \n
		No command help available \n
			:param scm_phi: No help available
		"""
		param = Conversions.decimal_value_to_str(scm_phi)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:PHI {param}')

	def get_sigma(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:SIGMa \n
		Snippet: value: float = driver.source.cemulation.scm.get_sigma() \n
		No command help available \n
			:return: sigma: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:SIGMa?')
		return Conversions.str_to_float(response)

	def set_sigma(self, sigma: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:SIGMa \n
		Snippet: driver.source.cemulation.scm.set_sigma(sigma = 1.0) \n
		No command help available \n
			:param sigma: No help available
		"""
		param = Conversions.decimal_value_to_str(sigma)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:SIGMa {param}')

	def get_speed(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:SPEed \n
		Snippet: value: float = driver.source.cemulation.scm.get_speed() \n
		No command help available \n
			:return: speed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:SPEed?')
		return Conversions.str_to_float(response)

	def set_speed(self, speed: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:SPEed \n
		Snippet: driver.source.cemulation.scm.set_speed(speed = 1.0) \n
		No command help available \n
			:param speed: No help available
		"""
		param = Conversions.decimal_value_to_str(speed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:SPEed {param}')

	def get_theta(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:THETa \n
		Snippet: value: float = driver.source.cemulation.scm.get_theta() \n
		No command help available \n
			:return: scm_theta: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:THETa?')
		return Conversions.str_to_float(response)

	def set_theta(self, scm_theta: float) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:THETa \n
		Snippet: driver.source.cemulation.scm.set_theta(scm_theta = 1.0) \n
		No command help available \n
			:param scm_theta: No help available
		"""
		param = Conversions.decimal_value_to_str(scm_theta)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:THETa {param}')

	def clone(self) -> 'ScmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
