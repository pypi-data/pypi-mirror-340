from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeedCls:
	"""Seed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seed", core, parent)

	def set(self, seed: int, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:HSDPa:HSET:SEED \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.seed.set(seed = 1, baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		Sets the seed for the random process deciding between the four options (see 'Randomly varying modulation and number of
		codes (Type 3i) settings') . \n
			:param seed: integer Range: 0 to 65535
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
		"""
		param = Conversions.decimal_value_to_str(seed)
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:HSDPa:HSET:SEED {param}')

	def get(self, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:HSDPa:HSET:SEED \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.seed.get(baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		Sets the seed for the random process deciding between the four options (see 'Randomly varying modulation and number of
		codes (Type 3i) settings') . \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: seed: integer Range: 0 to 65535"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:HSDPa:HSET:SEED?')
		return Conversions.str_to_int(response)
