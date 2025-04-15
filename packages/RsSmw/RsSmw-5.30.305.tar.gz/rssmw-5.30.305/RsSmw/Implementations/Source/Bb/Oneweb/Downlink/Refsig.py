from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefsigCls:
	"""Refsig commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("refsig", core, parent)

	def get_fpower(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:REFSig:FPOWer \n
		Snippet: value: float = driver.source.bb.oneweb.downlink.refsig.get_fpower() \n
		No command help available \n
			:return: first_power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:REFSig:FPOWer?')
		return Conversions.str_to_float(response)

	def set_fpower(self, first_power: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:REFSig:FPOWer \n
		Snippet: driver.source.bb.oneweb.downlink.refsig.set_fpower(first_power = 1.0) \n
		No command help available \n
			:param first_power: No help available
		"""
		param = Conversions.decimal_value_to_str(first_power)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:REFSig:FPOWer {param}')

	def get_power(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:REFSig:POWer \n
		Snippet: value: float = driver.source.bb.oneweb.downlink.refsig.get_power() \n
		Queries the reference signal power. \n
			:return: power: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:REFSig:POWer?')
		return Conversions.str_to_float(response)
