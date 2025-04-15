from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VelocityCls:
	"""Velocity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("velocity", core, parent)

	def get_ecef(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:VELocity:ECEF \n
		Snippet: value: bool = driver.source.bb.gnss.logging.category.satellite.velocity.get_ecef() \n
		Enables the parameter for logging. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:VELocity:ECEF?')
		return Conversions.str_to_bool(response)

	def set_ecef(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:VELocity:ECEF \n
		Snippet: driver.source.bb.gnss.logging.category.satellite.velocity.set_ecef(state = False) \n
		Enables the parameter for logging. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:VELocity:ECEF {param}')
