from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatusCls:
	"""Status commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("status", core, parent)

	def get(self, status: bool) -> bool:
		"""SCPI: [SOURce<HW>]:REGenerator:SIMulation:LEVel:VALid:[STATus] \n
		Snippet: value: bool = driver.source.regenerator.simulation.level.valid.status.get(status = False) \n
		Queries whether the calculated output level is within the permissible value range for the dedicated connector. \n
			:param status: 1| ON| 0| OFF
			:return: status: 1| ON| 0| OFF"""
		param = Conversions.bool_to_str(status)
		response = self._core.io.query_str(f'SOURce<HwInstance>:REGenerator:SIMulation:LEVel:VALid:STATus? {param}')
		return Conversions.str_to_bool(response)
