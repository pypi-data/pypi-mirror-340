from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RwindowCls:
	"""Rwindow commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rwindow", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def strajectory(self):
		"""strajectory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_strajectory'):
			from .Strajectory import StrajectoryCls
			self._strajectory = StrajectoryCls(self._core, self._cmd_group)
		return self._strajectory

	def set(self, rep_window: int, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:RWINdow \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.full.rwindow.set(rep_window = 1, vehicle = repcap.Vehicle.Default) \n
		Sets the repeating period (in km or s) of repeating objects. \n
			:param rep_window: integer Range: 0 to 1000
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = Conversions.decimal_value_to_str(rep_window)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:FULL:RWINdow {param}')

	def get(self, vehicle=repcap.Vehicle.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:RWINdow \n
		Snippet: value: int = driver.source.bb.gnss.receiver.v.environment.full.rwindow.get(vehicle = repcap.Vehicle.Default) \n
		Sets the repeating period (in km or s) of repeating objects. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: rep_window: integer Range: 0 to 1000"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:FULL:RWINdow?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'RwindowCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RwindowCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
