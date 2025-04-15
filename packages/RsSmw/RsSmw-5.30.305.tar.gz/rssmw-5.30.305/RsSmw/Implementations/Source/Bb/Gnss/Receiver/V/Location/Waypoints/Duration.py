from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DurationCls:
	"""Duration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("duration", core, parent)

	def set(self, duration: float, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:WAYPoints:DURation \n
		Snippet: driver.source.bb.gnss.receiver.v.location.waypoints.duration.set(duration = 1.0, vehicle = repcap.Vehicle.Default) \n
		Queries the trajectory duration. For R&S SMW-B9F and moving files with extension *.tle, you can set the duration. \n
			:param duration: float Range: 0 to depends on options
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = Conversions.decimal_value_to_str(duration)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:WAYPoints:DURation {param}')

	def get(self, vehicle=repcap.Vehicle.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:WAYPoints:DURation \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.location.waypoints.duration.get(vehicle = repcap.Vehicle.Default) \n
		Queries the trajectory duration. For R&S SMW-B9F and moving files with extension *.tle, you can set the duration. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: duration: float Range: 0 to depends on options"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:WAYPoints:DURation?')
		return Conversions.str_to_float(response)
