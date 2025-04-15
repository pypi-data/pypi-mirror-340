from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XonaCls:
	"""Xona commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xona", core, parent)

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:XONA:OFFSet \n
		Snippet: value: float = driver.source.bb.gnss.time.start.xona.get_offset() \n
		No command help available \n
			:return: utc_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:XONA:OFFSet?')
		return Conversions.str_to_float(response)

	def get_to_week(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:XONA:TOWeek \n
		Snippet: value: float = driver.source.bb.gnss.time.start.xona.get_to_week() \n
		No command help available \n
			:return: tow: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:XONA:TOWeek?')
		return Conversions.str_to_float(response)

	def get_wnumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:XONA:WNUMber \n
		Snippet: value: int = driver.source.bb.gnss.time.start.xona.get_wnumber() \n
		No command help available \n
			:return: system_week_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:XONA:WNUMber?')
		return Conversions.str_to_int(response)
