from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NapCls:
	"""Nap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nap", core, parent)

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsNap:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MTHRee:NAP \n
		Snippet: value: enums.BtoCsNap = driver.source.bb.btooth.cs.sevent.mthree.nap.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the number of antenna path in the N_AP field for Mode-2 and Mode-3 CS steps. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: nap: NAP_1| NAP_2| NAP_3| NAP_4 NAP_x, x represents the path number."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MTHRee:NAP?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsNap)
