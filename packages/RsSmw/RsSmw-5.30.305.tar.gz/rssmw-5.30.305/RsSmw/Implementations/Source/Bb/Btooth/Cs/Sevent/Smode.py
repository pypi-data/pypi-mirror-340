from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SmodeCls:
	"""Smode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("smode", core, parent)

	def set(self, sub_mode: enums.BtoCsSubMode, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:SMODe \n
		Snippet: driver.source.bb.btooth.cs.sevent.smode.set(sub_mode = enums.BtoCsSubMode.MODE1, channelNull = repcap.ChannelNull.Default) \n
		Sets the submode of the main mode. \n
			:param sub_mode: MODE1| MODE2| MODE3| NONE See the table Table 'CS step main modes and submodes' for an overview on available submodes per main mode.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(sub_mode, enums.BtoCsSubMode)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:SMODe {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsSubMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:SMODe \n
		Snippet: value: enums.BtoCsSubMode = driver.source.bb.btooth.cs.sevent.smode.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the submode of the main mode. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: sub_mode: MODE1| MODE2| MODE3| NONE See the table Table 'CS step main modes and submodes' for an overview on available submodes per main mode."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSubMode)
