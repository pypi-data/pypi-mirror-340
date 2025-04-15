from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScontentCls:
	"""Scontent commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scontent", core, parent)

	def set(self, seq_content: str, bitcount: int, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:SCONtent \n
		Snippet: driver.source.bb.btooth.cs.sevent.step.scontent.set(seq_content = rawAbc, bitcount = 1, channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		Queries the content and the length of a sounding sequence or random sequence. The content depends on the subevent mode.
		For CS test packets, you can set the content for a sounding sequence and random sequence. \n
			:param seq_content: numeric
			:param bitcount: integer Range: 32 to 128
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('seq_content', seq_content, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:SCONtent {param}'.rstrip())

	# noinspection PyTypeChecker
	class ScontentStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Seq_Content: str: numeric
			- 2 Bitcount: int: integer Range: 32 to 128"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Seq_Content'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Seq_Content: str = None
			self.Bitcount: int = None

	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> ScontentStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:SCONtent \n
		Snippet: value: ScontentStruct = driver.source.bb.btooth.cs.sevent.step.scontent.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		Queries the content and the length of a sounding sequence or random sequence. The content depends on the subevent mode.
		For CS test packets, you can set the content for a sounding sequence and random sequence. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: structure: for return value, see the help for ScontentStruct structure arguments."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:SCONtent?', self.__class__.ScontentStruct())
