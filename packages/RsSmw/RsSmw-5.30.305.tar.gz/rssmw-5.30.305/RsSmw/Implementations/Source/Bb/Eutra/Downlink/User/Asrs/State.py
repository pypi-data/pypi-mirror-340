from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, cu_ap_srs_state: bool, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:ASRS:STATe \n
		Snippet: driver.source.bb.eutra.downlink.user.asrs.state.set(cu_ap_srs_state = False, userIx = repcap.UserIx.Default) \n
		Enables/disables an aperiodic transmission of SRS for the selected user. \n
			:param cu_ap_srs_state: 1| ON| 0| OFF
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(cu_ap_srs_state)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:ASRS:STATe {param}')

	def get(self, userIx=repcap.UserIx.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:ASRS:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.downlink.user.asrs.state.get(userIx = repcap.UserIx.Default) \n
		Enables/disables an aperiodic transmission of SRS for the selected user. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: cu_ap_srs_state: 1| ON| 0| OFF"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:ASRS:STATe?')
		return Conversions.str_to_bool(response)
