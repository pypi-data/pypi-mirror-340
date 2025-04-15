from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalcCls:
	"""Calc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calc", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AntModCalcGeoMode:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:CALC:MODE \n
		Snippet: value: enums.AntModCalcGeoMode = driver.source.cemulation.scm.antenna.rx.calc.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:CALC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AntModCalcGeoMode)

	def set_mode(self, mode: enums.AntModCalcGeoMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:CALC:MODE \n
		Snippet: driver.source.cemulation.scm.antenna.rx.calc.set_mode(mode = enums.AntModCalcGeoMode.BFORming) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AntModCalcGeoMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:CALC:MODE {param}')
