from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TipoCls:
	"""Tipo commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tipo", core, parent)

	def set(self, tipo: enums.BtoCsTiP1, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MONE:TIPO \n
		Snippet: driver.source.bb.btooth.cs.sevent.mone.tipo.set(tipo = enums.BtoCsTiP1.TIP1_10, channelNull = repcap.ChannelNull.Default) \n
		Sets the time 'T_IP1' for Mode-0 and Mode-1 CS steps. \n
			:param tipo: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145 TIP1_x, x represents values in microseconds.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(tipo, enums.BtoCsTiP1)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MONE:TIPO {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MONE:TIPO \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.sevent.mone.tipo.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the time 'T_IP1' for Mode-0 and Mode-1 CS steps. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: tipo: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145 TIP1_x, x represents values in microseconds."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MONE:TIPO?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)
