from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqLengthCls:
	"""SeqLength commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seqLength", core, parent)

	def set(self, seq_len: enums.BtoCsSequenceLen, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:SEQLength \n
		Snippet: driver.source.bb.btooth.cs.sevent.seqLength.set(seq_len = enums.BtoCsSequenceLen.SL_0, channelNull = repcap.ChannelNull.Default) \n
		Sets the sequence length. The length is discrete and depends on the sequence type. Setting a sequence length of 0 bits
		requires manual step scheduling and Mode-1 or Mode-3 as the CS step main mode: SOURce1:BB:BTOoth:CS:SSCHeduling MANual
		SOURce1:BB:BTOoth:CS:MMODe MODE1 This 0-bit sequence is a CS sequence with no payload. \n
			:param seq_len: SL_0| SL_32| SL_64| SL_96| SL_128 Sequence length SL_x. x is the length in bits.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(seq_len, enums.BtoCsSequenceLen)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:SEQLength {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsSequenceLen:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:SEQLength \n
		Snippet: value: enums.BtoCsSequenceLen = driver.source.bb.btooth.cs.sevent.seqLength.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the sequence length. The length is discrete and depends on the sequence type. Setting a sequence length of 0 bits
		requires manual step scheduling and Mode-1 or Mode-3 as the CS step main mode: SOURce1:BB:BTOoth:CS:SSCHeduling MANual
		SOURce1:BB:BTOoth:CS:MMODe MODE1 This 0-bit sequence is a CS sequence with no payload. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: seq_len: SL_0| SL_32| SL_64| SL_96| SL_128 Sequence length SL_x. x is the length in bits."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:SEQLength?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSequenceLen)
