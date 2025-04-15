from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RowsCls:
	"""Rows commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rows", core, parent)

	# noinspection PyTypeChecker
	def get_size(self) -> enums.SystConfFadEntOutp:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:ROWS:[SIZE] \n
		Snippet: value: enums.SystConfFadEntOutp = driver.source.cemulation.scm.antenna.rx.rows.get_size() \n
		No command help available \n
			:return: num_rx_row: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:ROWS:SIZE?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfFadEntOutp)
