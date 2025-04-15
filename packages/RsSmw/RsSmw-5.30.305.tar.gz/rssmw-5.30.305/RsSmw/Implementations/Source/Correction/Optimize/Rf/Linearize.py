from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LinearizeCls:
	"""Linearize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("linearize", core, parent)

	def get_adjust(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:LINearize:ADJust \n
		Snippet: value: bool = driver.source.correction.optimize.rf.linearize.get_adjust() \n
		Measures the AM/AM nonlinearity on the RF chain for the current frequency. During the measurement, the instrument
		interrupts signal generation. \n
			:return: adjust_result: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:RF:LINearize:ADJust?')
		return Conversions.str_to_bool(response)
