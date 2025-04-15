from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClockCls:
	"""Clock commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_rate(self) -> enums.BbClock:
		"""SCPI: [SOURce<HW>]:CEMulation:CLOCk:RATE \n
		Snippet: value: enums.BbClock = driver.source.cemulation.clock.get_rate() \n
		No command help available \n
			:return: cloc_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CLOCk:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.BbClock)
