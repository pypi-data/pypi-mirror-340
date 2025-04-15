from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CountCls:
	"""Count commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("count", core, parent)

	def set(self, number_of_antenna: int, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ANTenna:COUNt \n
		Snippet: driver.source.bb.gnss.receiver.v.antenna.count.set(number_of_antenna = 1, vehicle = repcap.Vehicle.Default) \n
		Sets the number of simulated antennas. For more information, refer to the specifications document. \n
			:param number_of_antenna: integer Range: 1 to depends on the instrument
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = Conversions.decimal_value_to_str(number_of_antenna)
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ANTenna:COUNt {param}')

	def get(self, vehicle=repcap.Vehicle.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ANTenna:COUNt \n
		Snippet: value: int = driver.source.bb.gnss.receiver.v.antenna.count.get(vehicle = repcap.Vehicle.Default) \n
		Sets the number of simulated antennas. For more information, refer to the specifications document. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: number_of_antenna: integer Range: 1 to depends on the instrument"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:ANTenna:COUNt?')
		return Conversions.str_to_int(response)
