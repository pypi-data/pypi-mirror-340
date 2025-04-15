from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PzCls:
	"""Pz commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pz", core, parent)

	def set(self, longitude: float, latitude: float, altitude: float, baseSt=repcap.BaseSt.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:COORdinates:DECimal:PZ \n
		Snippet: driver.source.bb.gnss.rtk.base.location.coordinates.decimal.pz.set(longitude = 1.0, latitude = 1.0, altitude = 1.0, baseSt = repcap.BaseSt.Default) \n
		Defines the coordinates of the geographic location of the RTK base station in decimal format. \n
			:param longitude: float Defines the longitude in degrees. Range: -180 to 180
			:param latitude: float Defines the latitude in degrees. Range: -90 to 90
			:param altitude: float Defines the altitude. The altitude value is in meters and is the height above the reference ellipsoid. Range: -10E3 to 50E6
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('longitude', longitude, DataType.Float), ArgSingle('latitude', latitude, DataType.Float), ArgSingle('altitude', altitude, DataType.Float))
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:COORdinates:DECimal:PZ {param}'.rstrip())

	# noinspection PyTypeChecker
	class PzStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Longitude: float: float Defines the longitude in degrees. Range: -180 to 180
			- 2 Latitude: float: float Defines the latitude in degrees. Range: -90 to 90
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

	def get(self, baseSt=repcap.BaseSt.Default) -> PzStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:COORdinates:DECimal:PZ \n
		Snippet: value: PzStruct = driver.source.bb.gnss.rtk.base.location.coordinates.decimal.pz.get(baseSt = repcap.BaseSt.Default) \n
		Defines the coordinates of the geographic location of the RTK base station in decimal format. \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:return: structure: for return value, see the help for PzStruct structure arguments."""
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:COORdinates:DECimal:PZ?', self.__class__.PzStruct())
