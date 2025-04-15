from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:OFFSet:STATe \n
		Snippet: driver.sense.power.offset.state.set(state = False, channel = repcap.Channel.Default) \n
		Activates the addition of the level offset to the measured value. The level offset value is set with command method RsSmw.
		Sense.Power.Offset.set. \n
			:param state: 1| ON| 0| OFF
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:OFFSet:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: SENSe<CH>:[POWer]:OFFSet:STATe \n
		Snippet: value: bool = driver.sense.power.offset.state.get(channel = repcap.Channel.Default) \n
		Activates the addition of the level offset to the measured value. The level offset value is set with command method RsSmw.
		Sense.Power.Offset.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: state: 1| ON| 0| OFF"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:OFFSet:STATe?')
		return Conversions.str_to_bool(response)
