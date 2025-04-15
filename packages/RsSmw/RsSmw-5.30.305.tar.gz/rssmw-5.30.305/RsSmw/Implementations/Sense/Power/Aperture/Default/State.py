from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, use_def_ap: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:APERture:DEFault:STATe \n
		Snippet: driver.sense.power.aperture.default.state.set(use_def_ap = False, channel = repcap.Channel.Default) \n
		Deactivates the default aperture time of the respective sensor. To specify a user-defined value, use the command method
		RsSmw.Sense.Power.Aperture.Time.set. \n
			:param use_def_ap: 1| ON| 0| OFF
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.bool_to_str(use_def_ap)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:APERture:DEFault:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: SENSe<CH>:[POWer]:APERture:DEFault:STATe \n
		Snippet: value: bool = driver.sense.power.aperture.default.state.get(channel = repcap.Channel.Default) \n
		Deactivates the default aperture time of the respective sensor. To specify a user-defined value, use the command method
		RsSmw.Sense.Power.Aperture.Time.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: use_def_ap: 1| ON| 0| OFF"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:APERture:DEFault:STATe?')
		return Conversions.str_to_bool(response)
