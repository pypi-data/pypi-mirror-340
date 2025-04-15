from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdopplerCls:
	"""Fdoppler commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdoppler", core, parent)

	def get_actual(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:FDOPpler:ACTual \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.fdoppler.get_actual() \n
		No command help available \n
			:return: act_doppler: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:FDOPpler:ACTual?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:TCINterferer:MOVing:FDOPpler \n
		Snippet: value: float = driver.source.cemulation.tcInterferer.moving.fdoppler.get_value() \n
		No command help available \n
			:return: fdoppler: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TCINterferer:MOVing:FDOPpler?')
		return Conversions.str_to_float(response)
