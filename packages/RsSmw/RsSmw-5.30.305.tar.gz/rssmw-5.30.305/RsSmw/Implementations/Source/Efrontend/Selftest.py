from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelftestCls:
	"""Selftest commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("selftest", core, parent)

	def get_result(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:SELFtest:RESult \n
		Snippet: value: str = driver.source.efrontend.selftest.get_result() \n
		No command help available \n
			:return: fe_selftest_res: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:SELFtest:RESult?')
		return trim_str_response(response)

	def get_value(self) -> bool:
		"""SCPI: [SOURce<HW>]:EFRontend:SELFtest \n
		Snippet: value: bool = driver.source.efrontend.selftest.get_value() \n
		No command help available \n
			:return: success: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:SELFtest?')
		return Conversions.str_to_bool(response)
