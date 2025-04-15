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
	def get_size(self) -> enums.NumbSystAntenna:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:RX:ROWS:SIZE \n
		Snippet: value: enums.NumbSystAntenna = driver.source.cemulation.mimo.antenna.rx.rows.get_size() \n
		No command help available \n
			:return: ant_mod_rx_row_size: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MIMO:ANTenna:RX:ROWS:SIZE?')
		return Conversions.str_to_scalar_enum(response, enums.NumbSystAntenna)

	def set_size(self, ant_mod_rx_row_size: enums.NumbSystAntenna) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:RX:ROWS:SIZE \n
		Snippet: driver.source.cemulation.mimo.antenna.rx.rows.set_size(ant_mod_rx_row_size = enums.NumbSystAntenna.ANT01) \n
		No command help available \n
			:param ant_mod_rx_row_size: No help available
		"""
		param = Conversions.enum_scalar_to_str(ant_mod_rx_row_size, enums.NumbSystAntenna)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:ANTenna:RX:ROWS:SIZE {param}')
