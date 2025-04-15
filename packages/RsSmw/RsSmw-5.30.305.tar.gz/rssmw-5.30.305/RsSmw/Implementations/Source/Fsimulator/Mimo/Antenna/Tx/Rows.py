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
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:ANTenna:TX:ROWS:SIZE \n
		Snippet: value: enums.NumbSystAntenna = driver.source.fsimulator.mimo.antenna.tx.rows.get_size() \n
		Sets the number of rows and the number of columns in the antenna array. \n
			:return: ant_mod_tx_row_size: ANT01| ANT02| ANT03| ANT04| ANT08
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:MIMO:ANTenna:TX:ROWS:SIZE?')
		return Conversions.str_to_scalar_enum(response, enums.NumbSystAntenna)

	def set_size(self, ant_mod_tx_row_size: enums.NumbSystAntenna) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:ANTenna:TX:ROWS:SIZE \n
		Snippet: driver.source.fsimulator.mimo.antenna.tx.rows.set_size(ant_mod_tx_row_size = enums.NumbSystAntenna.ANT01) \n
		Sets the number of rows and the number of columns in the antenna array. \n
			:param ant_mod_tx_row_size: ANT01| ANT02| ANT03| ANT04| ANT08
		"""
		param = Conversions.enum_scalar_to_str(ant_mod_tx_row_size, enums.NumbSystAntenna)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:MIMO:ANTenna:TX:ROWS:SIZE {param}')
