from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EphemerisCls:
	"""Ephemeris commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ephemeris", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:CATalog \n
		Snippet: value: List[str] = driver.source.fsimulator.dsSimulation.user.tx.trajectory.ephemeris.get_catalog() \n
		No command help available \n
			:return: filenames: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:SELect \n
		Snippet: value: str = driver.source.fsimulator.dsSimulation.user.tx.trajectory.ephemeris.get_select() \n
		No command help available \n
			:return: traj_eph_select: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:SELect?')
		return trim_str_response(response)

	def set_select(self, traj_eph_select: str) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:SELect \n
		Snippet: driver.source.fsimulator.dsSimulation.user.tx.trajectory.ephemeris.set_select(traj_eph_select = 'abc') \n
		No command help available \n
			:param traj_eph_select: No help available
		"""
		param = Conversions.value_to_quoted_str(traj_eph_select)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:DSSimulation:USER:TX:TRAJectory:EPHemeris:SELect {param}')
