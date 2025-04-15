from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ShapingCls:
	"""Shaping commands group definition. 22 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("shaping", core, parent)

	@property
	def normalized(self):
		"""normalized commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_normalized'):
			from .Normalized import NormalizedCls
			self._normalized = NormalizedCls(self._core, self._cmd_group)
		return self._normalized

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def polynomial(self):
		"""polynomial commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_polynomial'):
			from .Polynomial import PolynomialCls
			self._polynomial = PolynomialCls(self._core, self._cmd_group)
		return self._polynomial

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def table(self):
		"""table commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_table'):
			from .Table import TableCls
			self._table = TableCls(self._core, self._cmd_group)
		return self._table

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DohertyShapeMode:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:MODE \n
		Snippet: value: enums.DohertyShapeMode = driver.source.iq.doherty.shaping.get_mode() \n
		Selects the method to define the correction coefficients. \n
			:return: shaping: TABLe| POLYnomial| NORMalized| DOHerty
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:SHAPing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DohertyShapeMode)

	def set_mode(self, shaping: enums.DohertyShapeMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:MODE \n
		Snippet: driver.source.iq.doherty.shaping.set_mode(shaping = enums.DohertyShapeMode.DOHerty) \n
		Selects the method to define the correction coefficients. \n
			:param shaping: TABLe| POLYnomial| NORMalized| DOHerty
		"""
		param = Conversions.enum_scalar_to_str(shaping, enums.DohertyShapeMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:MODE {param}')

	def clone(self) -> 'ShapingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ShapingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
