from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sp5KCls:
	"""Sp5K commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sp5K", core, parent)

	def get_trtsamples(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP5K:TRTSamples \n
		Snippet: value: int = driver.source.bb.nr5G.output.tdWind.sp5K.get_trtsamples() \n
		No command help available \n
			:return: transition_sampl: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP5K:TRTSamples?')
		return Conversions.str_to_int(response)

	def get_tr_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP5K:TRTime \n
		Snippet: value: float = driver.source.bb.nr5G.output.tdWind.sp5K.get_tr_time() \n
		No command help available \n
			:return: transition_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP5K:TRTime?')
		return Conversions.str_to_float(response)
