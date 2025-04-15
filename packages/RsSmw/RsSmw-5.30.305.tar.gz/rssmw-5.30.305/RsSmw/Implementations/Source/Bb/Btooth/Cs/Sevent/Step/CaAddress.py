from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CaAddressCls:
	"""CaAddress commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("caAddress", core, parent)

	def set(self, access_address: str, bitcount: int, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CAADdress \n
		Snippet: driver.source.bb.btooth.cs.sevent.step.caAddress.set(access_address = rawAbc, bitcount = 1, channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		Sets or queries the 32-bit CS access address for individual CS steps. Setting require manual step scheduling:
		SOURce1::BB:BTOoth:CS:SSCHeduling MANUAL See also [:SOURce<hw>]:BB:BTOoth:CS:SSCHeduling. \n
			:param access_address: numeric
			:param bitcount: integer Range: 32 to 32
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('access_address', access_address, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CAADdress {param}'.rstrip())

	# noinspection PyTypeChecker
	class CaAddressStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Access_Address: str: numeric
			- 2 Bitcount: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Access_Address'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Access_Address: str = None
			self.Bitcount: int = None

	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> CaAddressStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CAADdress \n
		Snippet: value: CaAddressStruct = driver.source.bb.btooth.cs.sevent.step.caAddress.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		Sets or queries the 32-bit CS access address for individual CS steps. Setting require manual step scheduling:
		SOURce1::BB:BTOoth:CS:SSCHeduling MANUAL See also [:SOURce<hw>]:BB:BTOoth:CS:SSCHeduling. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: structure: for return value, see the help for CaAddressStruct structure arguments."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CAADdress?', self.__class__.CaAddressStruct())
