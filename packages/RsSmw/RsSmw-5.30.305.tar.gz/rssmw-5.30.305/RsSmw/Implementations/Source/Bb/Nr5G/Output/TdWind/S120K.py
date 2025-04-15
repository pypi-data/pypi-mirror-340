from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class S120KCls:
	"""S120K commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("s120K", core, parent)

	def get_trtsamples(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:S120K:TRTSamples \n
		Snippet: value: int = driver.source.bb.nr5G.output.tdWind.s120K.get_trtsamples() \n
		Queries the number of transition samples.
			INTRO_CMD_HELP: The next to last block in the command syntax indicates the used SCS and CP combination. \n
			- DL: SE<SCS>K, where E indicates the extended CP or for normal CP, the designation is omitted \n
			:return: transition_sampl: integer Range: 0 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:S120K:TRTSamples?')
		return Conversions.str_to_int(response)

	def get_tr_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:S120K:TRTime \n
		Snippet: value: float = driver.source.bb.nr5G.output.tdWind.s120K.get_tr_time() \n
		Sets the transition time when time domain windowing is active.
			INTRO_CMD_HELP: The next to last block in the command syntax indicates the used SCS and CP combination. \n
			- DL: SE<SCS>K, where E indicates the extended CP or for normal CP, the designation is omitted \n
			:return: transition_time: float Range: 0 to 1E-5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:S120K:TRTime?')
		return Conversions.str_to_float(response)
