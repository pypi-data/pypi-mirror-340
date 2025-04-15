from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XCls:
	"""X commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("x", core, parent)

	def set(self, xoffset: float, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:ROFFset:X \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.vobs.roffset.x.set(xoffset = 1.0, vehicle = repcap.Vehicle.Default) \n
		Sets the initial X position of a receiver relative to the reference point that is the (0, 0, 0) coordinate. \n
			:param xoffset: float Range: -1500 to 1500
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = Conversions.decimal_value_to_str(xoffset)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:VOBS:ROFFset:X {param}')

	def get(self, vehicle=repcap.Vehicle.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:ROFFset:X \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.environment.vobs.roffset.x.get(vehicle = repcap.Vehicle.Default) \n
		Sets the initial X position of a receiver relative to the reference point that is the (0, 0, 0) coordinate. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: xoffset: float Range: -1500 to 1500"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ENVironment:VOBS:ROFFset:X?')
		return Conversions.str_to_float(response)
