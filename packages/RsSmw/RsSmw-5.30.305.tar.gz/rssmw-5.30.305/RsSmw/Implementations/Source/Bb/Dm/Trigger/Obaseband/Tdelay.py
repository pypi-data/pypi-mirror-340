from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdelayCls:
	"""Tdelay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdelay", core, parent)

	def set(self, obas_time_delay: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband<CH>:TDELay \n
		Snippet: driver.source.bb.dm.trigger.obaseband.tdelay.set(obas_time_delay = 1.0, channel = repcap.Channel.Default) \n
		Sets the trigger delay for triggering by the signal from the other path. \n
			:param obas_time_delay: float Range: 0 to 7929.170398682, Unit: s
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Obaseband')
		"""
		param = Conversions.decimal_value_to_str(obas_time_delay)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:OBASeband{channel_cmd_val}:TDELay {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband<CH>:TDELay \n
		Snippet: value: float = driver.source.bb.dm.trigger.obaseband.tdelay.get(channel = repcap.Channel.Default) \n
		Sets the trigger delay for triggering by the signal from the other path. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Obaseband')
			:return: obas_time_delay: float Range: 0 to 7929.170398682, Unit: s"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DM:TRIGger:OBASeband{channel_cmd_val}:TDELay?')
		return Conversions.str_to_float(response)
