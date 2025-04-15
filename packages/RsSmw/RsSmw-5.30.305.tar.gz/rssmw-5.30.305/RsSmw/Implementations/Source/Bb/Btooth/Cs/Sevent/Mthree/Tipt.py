from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TiptCls:
	"""Tipt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tipt", core, parent)

	def set(self, tipt: enums.BtoCsTiP2, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MTHRee:TIPT \n
		Snippet: driver.source.bb.btooth.cs.sevent.mthree.tipt.set(tipt = enums.BtoCsTiP2.TIP2_10, channelNull = repcap.ChannelNull.Default) \n
		Sets the time 'T_IP2' for Mode-2 or Mode-3 CS steps. \n
			:param tipt: TIP2_10| TIP2_20| TIP2_30| TIP2_40| TIP2_50| TIP2_60| TIP2_80| TIP2_145 TIP2_x, x represents values in microseconds.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(tipt, enums.BtoCsTiP2)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MTHRee:TIPT {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsTiP2:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MTHRee:TIPT \n
		Snippet: value: enums.BtoCsTiP2 = driver.source.bb.btooth.cs.sevent.mthree.tipt.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the time 'T_IP2' for Mode-2 or Mode-3 CS steps. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: tipt: TIP2_10| TIP2_20| TIP2_30| TIP2_40| TIP2_50| TIP2_60| TIP2_80| TIP2_145 TIP2_x, x represents values in microseconds."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MTHRee:TIPT?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP2)
