from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UdtCls:
	"""Udt commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("udt", core, parent)

	def get_cycle(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:CYCLe \n
		Snippet: value: int = driver.source.bb.oneweb.udt.get_cycle() \n
		No command help available \n
			:return: cycle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UDT:CYCLe?')
		return Conversions.str_to_int(response)

	def set_cycle(self, cycle: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:CYCLe \n
		Snippet: driver.source.bb.oneweb.udt.set_cycle(cycle = 1) \n
		No command help available \n
			:param cycle: No help available
		"""
		param = Conversions.decimal_value_to_str(cycle)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UDT:CYCLe {param}')

	def get_on_duration(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:ONDuration \n
		Snippet: value: int = driver.source.bb.oneweb.udt.get_on_duration() \n
		No command help available \n
			:return: on_duration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UDT:ONDuration?')
		return Conversions.str_to_int(response)

	def set_on_duration(self, on_duration: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:ONDuration \n
		Snippet: driver.source.bb.oneweb.udt.set_on_duration(on_duration = 1) \n
		No command help available \n
			:param on_duration: No help available
		"""
		param = Conversions.decimal_value_to_str(on_duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UDT:ONDuration {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:STATe \n
		Snippet: value: bool = driver.source.bb.oneweb.udt.get_state() \n
		No command help available \n
			:return: test_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:UDT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, test_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UDT:STATe \n
		Snippet: driver.source.bb.oneweb.udt.set_state(test_state = False) \n
		No command help available \n
			:param test_state: No help available
		"""
		param = Conversions.bool_to_str(test_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:UDT:STATe {param}')
