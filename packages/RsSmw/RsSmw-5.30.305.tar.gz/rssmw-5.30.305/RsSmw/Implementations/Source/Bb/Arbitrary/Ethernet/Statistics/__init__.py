from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatisticsCls:
	"""Statistics commands group definition. 9 total commands, 8 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("statistics", core, parent)

	@property
	def errors(self):
		"""errors commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_errors'):
			from .Errors import ErrorsCls
			self._errors = ErrorsCls(self._core, self._cmd_group)
		return self._errors

	@property
	def rxbLive(self):
		"""rxbLive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxbLive'):
			from .RxbLive import RxbLiveCls
			self._rxbLive = RxbLiveCls(self._core, self._cmd_group)
		return self._rxbLive

	@property
	def rxbMin(self):
		"""rxbMin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxbMin'):
			from .RxbMin import RxbMinCls
			self._rxbMin = RxbMinCls(self._core, self._cmd_group)
		return self._rxbMin

	@property
	def rxcFrames(self):
		"""rxcFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxcFrames'):
			from .RxcFrames import RxcFramesCls
			self._rxcFrames = RxcFramesCls(self._core, self._cmd_group)
		return self._rxcFrames

	@property
	def rxdBytes(self):
		"""rxdBytes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxdBytes'):
			from .RxdBytes import RxdBytesCls
			self._rxdBytes = RxdBytesCls(self._core, self._cmd_group)
		return self._rxdBytes

	@property
	def rxdFrames(self):
		"""rxdFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxdFrames'):
			from .RxdFrames import RxdFramesCls
			self._rxdFrames = RxdFramesCls(self._core, self._cmd_group)
		return self._rxdFrames

	@property
	def rxuSegments(self):
		"""rxuSegments commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxuSegments'):
			from .RxuSegments import RxuSegmentsCls
			self._rxuSegments = RxuSegmentsCls(self._core, self._cmd_group)
		return self._rxuSegments

	@property
	def txrFrames(self):
		"""txrFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txrFrames'):
			from .TxrFrames import TxrFramesCls
			self._txrFrames = TxrFramesCls(self._core, self._cmd_group)
		return self._txrFrames

	# noinspection PyTypeChecker
	class AllStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Rx_Upload_Segment: int: integer Number of Rx upload segments, see [:SOURcehw]:BB:ARBitrary:ETHernet:STATistics:RXUSegments?.
			- Rx_Control_Frames: int: integer Number of Rx control frames, see [:SOURcehw]:BB:ARBitrary:ETHernet:STATistics:RXCFrames?.
			- Rx_Data_Frames: int: integer Number of Rx data frames, see [:SOURcehw]:BB:ARBitrary:ETHernet:STATistics:RXCFrames?.
			- Rx_Data_Bytes: int: integer Number of Rx data bytes, see [:SOURcehw]:BB:ARBitrary:ETHernet:STATistics:RXDBytes?.
			- Tx_Reply_Frames: int: integer Number of Tx reply frames, see [:SOURcehw]:BB:ARBitrary:ETHernet:STATistics:TXRFrames?."""
		__meta_args_list = [
			ArgStruct.scalar_int('Rx_Upload_Segment'),
			ArgStruct.scalar_int('Rx_Control_Frames'),
			ArgStruct.scalar_int('Rx_Data_Frames'),
			ArgStruct.scalar_int('Rx_Data_Bytes'),
			ArgStruct.scalar_int('Tx_Reply_Frames')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Upload_Segment: int = None
			self.Rx_Control_Frames: int = None
			self.Rx_Data_Frames: int = None
			self.Rx_Data_Bytes: int = None
			self.Tx_Reply_Frames: int = None

	def get_all(self) -> AllStruct:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:STATistics:ALL \n
		Snippet: value: AllStruct = driver.source.bb.arbitrary.ethernet.statistics.get_all() \n
		Queries all statistic results in a comma-separated list that contains the following parameters: <RxUploadSegments>,
		<RxConrolFrames>,<RxDataFrames>,<RxDataBytes>,<TxReplyFrames>,<OccuredErrors> \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:ARBitrary:ETHernet:STATistics:ALL?', self.__class__.AllStruct())

	def clone(self) -> 'StatisticsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StatisticsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
