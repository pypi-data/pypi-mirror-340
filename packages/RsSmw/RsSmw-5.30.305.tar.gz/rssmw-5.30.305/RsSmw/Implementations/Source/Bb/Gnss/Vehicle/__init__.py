from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VehicleCls:
	"""Vehicle commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vehicle", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def get_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:VEHicle:COUNt \n
		Snippet: value: int = driver.source.bb.gnss.vehicle.get_count() \n
		Sets the number of simulated vehicles. \n
			:return: number_of_vehicle: integer Range: 1 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:VEHicle:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, number_of_vehicle: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:VEHicle:COUNt \n
		Snippet: driver.source.bb.gnss.vehicle.set_count(number_of_vehicle = 1) \n
		Sets the number of simulated vehicles. \n
			:param number_of_vehicle: integer Range: 1 to 2
		"""
		param = Conversions.decimal_value_to_str(number_of_vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:VEHicle:COUNt {param}')

	def clone(self) -> 'VehicleCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = VehicleCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
