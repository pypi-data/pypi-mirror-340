from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AggregateCls:
	"""Aggregate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aggregate", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:AGGRegate:STATe \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.hda.aggregate.get_state() \n
		Queries the channel aggregate state that is off. \n
			:return: aggregate: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:AGGRegate:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, aggregate: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:AGGRegate:STATe \n
		Snippet: driver.source.bb.wlay.pconfig.hda.aggregate.set_state(aggregate = False) \n
		Queries the channel aggregate state that is off. \n
			:param aggregate: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(aggregate)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:AGGRegate:STATe {param}')
