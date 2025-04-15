from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DecimalCls:
	"""Decimal commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("decimal", core, parent)

	def set(self, longitude: float, latitude: float, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DFLocation:COORdinates:DECimal \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.dfLocation.coordinates.decimal.set(longitude = 1.0, latitude = 1.0, vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Defines the coordinates of the Delta FPAD location in decimal format. \n
			:param longitude: float Range: -1.0 to 1.0
			:param latitude: float Range: -1.0 to 1.0
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('longitude', longitude, DataType.Float), ArgSingle('latitude', latitude, DataType.Float))
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DFLocation:COORdinates:DECimal {param}'.rstrip())

	# noinspection PyTypeChecker
	class DecimalStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Longitude: float: float Range: -1.0 to 1.0
			- 2 Latitude: float: float Range: -1.0 to 1.0"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> DecimalStruct:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DFLocation:COORdinates:DECimal \n
		Snippet: value: DecimalStruct = driver.source.bb.gbas.vdb.mconfig.dfLocation.coordinates.decimal.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Defines the coordinates of the Delta FPAD location in decimal format. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: structure: for return value, see the help for DecimalStruct structure arguments."""
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DFLocation:COORdinates:DECimal?', self.__class__.DecimalStruct())
