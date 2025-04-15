from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TswCls:
	"""Tsw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsw", core, parent)

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsTsw:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MTWO:TSW \n
		Snippet: value: enums.BtoCsTsw = driver.source.bb.btooth.cs.sevent.mtwo.tsw.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the time 'T_SW' for Mode-2 or Mode-3 CS steps. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: tsw: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10 TSW_x, x represents values in microseconds."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MTWO:TSW?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTsw)
