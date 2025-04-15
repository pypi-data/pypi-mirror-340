from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxCls:
	"""Rx commands group definition. 8 total commands, 5 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rx", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .Antenna import AntennaCls
			self._antenna = AntennaCls(self._core, self._cmd_group)
		return self._antenna

	@property
	def calc(self):
		"""calc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_calc'):
			from .Calc import CalcCls
			self._calc = CalcCls(self._core, self._cmd_group)
		return self._calc

	@property
	def columns(self):
		"""columns commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_columns'):
			from .Columns import ColumnsCls
			self._columns = ColumnsCls(self._core, self._cmd_group)
		return self._columns

	@property
	def espacing(self):
		"""espacing commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_espacing'):
			from .Espacing import EspacingCls
			self._espacing = EspacingCls(self._core, self._cmd_group)
		return self._espacing

	@property
	def rows(self):
		"""rows commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rows'):
			from .Rows import RowsCls
			self._rows = RowsCls(self._core, self._cmd_group)
		return self._rows

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.AntMod3DaNtPattern:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:PATTern \n
		Snippet: value: enums.AntMod3DaNtPattern = driver.source.cemulation.scm.antenna.rx.get_pattern() \n
		No command help available \n
			:return: type_of_pattern: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.AntMod3DaNtPattern)

	def set_pattern(self, type_of_pattern: enums.AntMod3DaNtPattern) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:PATTern \n
		Snippet: driver.source.cemulation.scm.antenna.rx.set_pattern(type_of_pattern = enums.AntMod3DaNtPattern.DIPole) \n
		No command help available \n
			:param type_of_pattern: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_of_pattern, enums.AntMod3DaNtPattern)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:PATTern {param}')

	# noinspection PyTypeChecker
	def get_structure(self) -> enums.AntModStructure:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:STRucture \n
		Snippet: value: enums.AntModStructure = driver.source.cemulation.scm.antenna.rx.get_structure() \n
		No command help available \n
			:return: antenna_rx_struct: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:STRucture?')
		return Conversions.str_to_scalar_enum(response, enums.AntModStructure)

	def set_structure(self, antenna_rx_struct: enums.AntModStructure) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:STRucture \n
		Snippet: driver.source.cemulation.scm.antenna.rx.set_structure(antenna_rx_struct = enums.AntModStructure.CROSS) \n
		No command help available \n
			:param antenna_rx_struct: No help available
		"""
		param = Conversions.enum_scalar_to_str(antenna_rx_struct, enums.AntModStructure)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:STRucture {param}')

	def clone(self) -> 'RxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
