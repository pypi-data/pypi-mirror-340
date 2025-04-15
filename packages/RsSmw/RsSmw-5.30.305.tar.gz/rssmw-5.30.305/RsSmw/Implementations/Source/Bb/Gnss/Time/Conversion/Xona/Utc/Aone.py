from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AoneCls:
	"""Aone commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aone", core, parent)

	def get_unscaled(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.time.conversion.xona.utc.aone.get_unscaled() \n
		No command help available \n
			:return: a_1: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE:UNSCaled?')
		return Conversions.str_to_float(response)

	def set_unscaled(self, a_1: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE:UNSCaled \n
		Snippet: driver.source.bb.gnss.time.conversion.xona.utc.aone.set_unscaled(a_1 = 1.0) \n
		No command help available \n
			:param a_1: No help available
		"""
		param = Conversions.decimal_value_to_str(a_1)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE:UNSCaled {param}')

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.xona.utc.aone.get_value() \n
		No command help available \n
			:return: aone: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE?')
		return Conversions.str_to_int(response)

	def set_value(self, aone: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE \n
		Snippet: driver.source.bb.gnss.time.conversion.xona.utc.aone.set_value(aone = 1) \n
		No command help available \n
			:param aone: No help available
		"""
		param = Conversions.decimal_value_to_str(aone)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:XONA:UTC:AONE {param}')
