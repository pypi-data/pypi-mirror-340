from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrajectoryCls:
	"""Trajectory commands group definition. 12 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trajectory", core, parent)

	@property
	def ephemeris(self):
		"""ephemeris commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Ephemeris import EphemerisCls
			self._ephemeris = EphemerisCls(self._core, self._cmd_group)
		return self._ephemeris

	@property
	def fapoint(self):
		"""fapoint commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fapoint'):
			from .Fapoint import FapointCls
			self._fapoint = FapointCls(self._core, self._cmd_group)
		return self._fapoint

	@property
	def tdf(self):
		"""tdf commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_tdf'):
			from .Tdf import TdfCls
			self._tdf = TdfCls(self._core, self._cmd_group)
		return self._tdf

	# noinspection PyTypeChecker
	def get_value(self) -> enums.FadDssUsrTraj:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory \n
		Snippet: value: enums.FadDssUsrTraj = driver.source.fsimulator.dsSimulation.user.rx.trajectory.get_value() \n
		No command help available \n
			:return: trajectory: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory?')
		return Conversions.str_to_scalar_enum(response, enums.FadDssUsrTraj)

	def set_value(self, trajectory: enums.FadDssUsrTraj) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory \n
		Snippet: driver.source.fsimulator.dsSimulation.user.rx.trajectory.set_value(trajectory = enums.FadDssUsrTraj.EPHemeris) \n
		No command help available \n
			:param trajectory: No help available
		"""
		param = Conversions.enum_scalar_to_str(trajectory, enums.FadDssUsrTraj)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory {param}')

	def clone(self) -> 'TrajectoryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TrajectoryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
