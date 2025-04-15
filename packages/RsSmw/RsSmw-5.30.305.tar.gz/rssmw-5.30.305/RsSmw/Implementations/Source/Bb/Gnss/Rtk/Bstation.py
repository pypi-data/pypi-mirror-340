from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BstationCls:
	"""Bstation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bstation", core, parent)

	# noinspection PyTypeChecker
	def get_count(self) -> enums.NumberA:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BSTation:COUNt \n
		Snippet: value: enums.NumberA = driver.source.bb.gnss.rtk.bstation.get_count() \n
		Queries the number of RTK base stations. \n
			:return: number_of_bases: 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RTK:BSTation:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_count(self, number_of_bases: enums.NumberA) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BSTation:COUNt \n
		Snippet: driver.source.bb.gnss.rtk.bstation.set_count(number_of_bases = enums.NumberA._1) \n
		Queries the number of RTK base stations. \n
			:param number_of_bases: 1
		"""
		param = Conversions.enum_scalar_to_str(number_of_bases, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:BSTation:COUNt {param}')
