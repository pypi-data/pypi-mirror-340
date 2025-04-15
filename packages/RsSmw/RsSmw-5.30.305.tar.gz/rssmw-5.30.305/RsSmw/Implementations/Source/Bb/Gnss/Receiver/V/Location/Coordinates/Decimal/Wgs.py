from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WgsCls:
	"""Wgs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wgs", core, parent)

	def set(self, longitude: float, latitude: float, altitude: float, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: driver.source.bb.gnss.receiver.v.location.coordinates.decimal.wgs.set(longitude = 1.0, latitude = 1.0, altitude = 1.0, vehicle = repcap.Vehicle.Default) \n
		Defines the coordinates of the geographic location of the GNSS receiver in decimal format. \n
			:param longitude: float Defines the longitude. Range: -180 to 180
			:param latitude: float Defines the latitude. Range: -90 to 90
			:param altitude: float Defines the altitude. The altitude value is in meters and is the height above the reference ellipsoid. Range: -10E3 to 50E6
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('longitude', longitude, DataType.Float), ArgSingle('latitude', latitude, DataType.Float), ArgSingle('altitude', altitude, DataType.Float))
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:COORdinates:DECimal:WGS {param}'.rstrip())

	# noinspection PyTypeChecker
	class WgsStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Longitude: float: float Defines the longitude. Range: -180 to 180
			- 2 Latitude: float: float Defines the latitude. Range: -90 to 90
			- 3 Altitude: float: float Defines the altitude. The altitude value is in meters and is the height above the reference ellipsoid. Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def get(self, vehicle=repcap.Vehicle.Default) -> WgsStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: value: WgsStruct = driver.source.bb.gnss.receiver.v.location.coordinates.decimal.wgs.get(vehicle = repcap.Vehicle.Default) \n
		Defines the coordinates of the geographic location of the GNSS receiver in decimal format. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: structure: for return value, see the help for WgsStruct structure arguments."""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:COORdinates:DECimal:WGS?', self.__class__.WgsStruct())
