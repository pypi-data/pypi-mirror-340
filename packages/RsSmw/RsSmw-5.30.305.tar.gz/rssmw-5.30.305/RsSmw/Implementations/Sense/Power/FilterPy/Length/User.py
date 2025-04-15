from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, user: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:FILTer:LENGth:[USER] \n
		Snippet: driver.sense.power.filterPy.length.user.set(user = 1.0, channel = repcap.Channel.Default) \n
		Selects the filter length for SENS:POW:FILT:'TYPE USER. As the filter length works as a multiplier for the time window, a
		constant filter length results in a constant measurement time (see also 'About the measuring principle, averaging filter,
		filter length, and achieving stable results') . The R&S NRP power sensors provide different resolutions for setting the
		filter length, depending on the used sensor type. For more information, refer to the specifications document. \n
			:param user: float Range: 1 to depends on R&S NRP power sensor type
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(user)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:LENGth:USER {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:FILTer:LENGth:[USER] \n
		Snippet: value: float = driver.sense.power.filterPy.length.user.get(channel = repcap.Channel.Default) \n
		Selects the filter length for SENS:POW:FILT:'TYPE USER. As the filter length works as a multiplier for the time window, a
		constant filter length results in a constant measurement time (see also 'About the measuring principle, averaging filter,
		filter length, and achieving stable results') . The R&S NRP power sensors provide different resolutions for setting the
		filter length, depending on the used sensor type. For more information, refer to the specifications document. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: user: float Range: 1 to depends on R&S NRP power sensor type"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:LENGth:USER?')
		return Conversions.str_to_float(response)
