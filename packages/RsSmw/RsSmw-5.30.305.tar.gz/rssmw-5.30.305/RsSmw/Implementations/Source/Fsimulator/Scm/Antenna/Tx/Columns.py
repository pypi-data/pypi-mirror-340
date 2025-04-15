from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ColumnsCls:
	"""Columns commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("columns", core, parent)

	# noinspection PyTypeChecker
	def get_size(self) -> enums.SystConfFadEntOutp:
		"""SCPI: [SOURce<HW>]:FSIMulator:SCM:ANTenna:TX:COLumns:[SIZE] \n
		Snippet: value: enums.SystConfFadEntOutp = driver.source.fsimulator.scm.antenna.tx.columns.get_size() \n
		Queries the number of rows and the number of columns in the antenna array. \n
			:return: num_tx_col: R01| R02| R03| R04| R08
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:SCM:ANTenna:TX:COLumns:SIZE?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfFadEntOutp)

	def set_size(self, num_tx_col: enums.SystConfFadEntOutp) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:SCM:ANTenna:TX:COLumns:[SIZE] \n
		Snippet: driver.source.fsimulator.scm.antenna.tx.columns.set_size(num_tx_col = enums.SystConfFadEntOutp.R01) \n
		Queries the number of rows and the number of columns in the antenna array. \n
			:param num_tx_col: No help available
		"""
		param = Conversions.enum_scalar_to_str(num_tx_col, enums.SystConfFadEntOutp)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:SCM:ANTenna:TX:COLumns:SIZE {param}')
