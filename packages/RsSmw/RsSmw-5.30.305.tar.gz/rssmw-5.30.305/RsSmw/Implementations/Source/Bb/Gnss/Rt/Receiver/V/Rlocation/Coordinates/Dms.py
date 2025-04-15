from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmsCls:
	"""Dms commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dms", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Longitude_Deg: int: integer Range: 0 to 180
			- 2 Longitude_Min: int: integer Range: 0 to 59
			- 3 Longitude_Sec: float: float Range: 0 to 59.999
			- 4 Longitude_Dir: str: select
			- 5 Latitude_Deg: int: integer Range: 0 to 90
			- 6 Latitude_Min: int: integer Range: 0 to 59
			- 7 Latitude_Sec: float: float Range: 0 to 59.999
			- 8 Latitude_Dir: str: select
			- 9 Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_int('Longitude_Deg'),
			ArgStruct.scalar_int('Longitude_Min'),
			ArgStruct.scalar_float('Longitude_Sec'),
			ArgStruct.scalar_str('Longitude_Dir'),
			ArgStruct.scalar_int('Latitude_Deg'),
			ArgStruct.scalar_int('Latitude_Min'),
			ArgStruct.scalar_float('Latitude_Sec'),
			ArgStruct.scalar_str('Latitude_Dir'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude_Deg: int = None
			self.Longitude_Min: int = None
			self.Longitude_Sec: float = None
			self.Longitude_Dir: str = None
			self.Latitude_Deg: int = None
			self.Latitude_Min: int = None
			self.Latitude_Sec: float = None
			self.Latitude_Dir: str = None
			self.Altitude: float = None

	def get(self, time_basis: enums.TimeBasis, ycoorear: int, month: int, day: int, hour: int, minutes: int, seconds: float, week_number: int, time_of_week: float, vehicle=repcap.Vehicle.Default) -> GetStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:RECeiver:[V<ST>]:RLOCation:COORdinates:DMS \n
		Snippet: value: GetStruct = driver.source.bb.gnss.rt.receiver.v.rlocation.coordinates.dms.get(time_basis = enums.TimeBasis.BDT, ycoorear = 1, month = 1, day = 1, hour = 1, minutes = 1, seconds = 1.0, week_number = 1, time_of_week = 1.0, vehicle = repcap.Vehicle.Default) \n
		Queries the coordinates of the receiver location in DMS format for the selected moment of time. The required query
		parameters depend on the selected timebase. \n
			:param time_basis: select
			:param ycoorear: No help available
			:param month: integer Range: 1 to 12
			:param day: integer Range: 1 to 31
			:param hour: integer Range: 0 to 23
			:param minutes: integer Range: 0 to 59
			:param seconds: float Range: 0 to 59.999
			:param week_number: integer Range: 0 to 529947
			:param time_of_week: float Range: 0 to 604799.999
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('time_basis', time_basis, DataType.Enum, enums.TimeBasis), ArgSingle('ycoorear', ycoorear, DataType.Integer), ArgSingle('month', month, DataType.Integer), ArgSingle('day', day, DataType.Integer), ArgSingle('hour', hour, DataType.Integer), ArgSingle('minutes', minutes, DataType.Integer), ArgSingle('seconds', seconds, DataType.Float), ArgSingle('week_number', week_number, DataType.Integer), ArgSingle('time_of_week', time_of_week, DataType.Float))
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RT:RECeiver:V{vehicle_cmd_val}:RLOCation:COORdinates:DMS? {param}'.rstrip(), self.__class__.GetStruct())
