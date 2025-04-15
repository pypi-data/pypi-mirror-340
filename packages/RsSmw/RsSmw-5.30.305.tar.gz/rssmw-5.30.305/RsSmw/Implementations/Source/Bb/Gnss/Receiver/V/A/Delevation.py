from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelevationCls:
	"""Delevation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delevation", core, parent)

	def set(self, delta_elevation: float, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:DELevation \n
		Snippet: driver.source.bb.gnss.receiver.v.a.delevation.set(delta_elevation = 1.0, vehicle = repcap.Vehicle.Default, antenna = repcap.Antenna.Default) \n
		Sets the orientation and tilt of the antenna of the GNSS receiver. The values are relative to the center of gravity (COG)
		. \n
			:param delta_elevation: float Range: -180 to 180
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
		"""
		param = Conversions.decimal_value_to_str(delta_elevation)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._cmd_group.get_repcap_cmd_value(antenna, repcap.Antenna)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:A{antenna_cmd_val}:DELevation {param}')

	def get(self, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:DELevation \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.a.delevation.get(vehicle = repcap.Vehicle.Default, antenna = repcap.Antenna.Default) \n
		Sets the orientation and tilt of the antenna of the GNSS receiver. The values are relative to the center of gravity (COG)
		. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:return: delta_elevation: float Range: -180 to 180"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._cmd_group.get_repcap_cmd_value(antenna, repcap.Antenna)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:A{antenna_cmd_val}:DELevation?')
		return Conversions.str_to_float(response)
