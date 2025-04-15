from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SintervalCls:
	"""Sinterval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sinterval", core, parent)

	def set(self, user_sps_int: enums.SpsInt, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SINTerval \n
		Snippet: driver.source.bb.eutra.downlink.user.sps.sinterval.set(user_sps_int = enums.SpsInt.S10, userIx = repcap.UserIx.Default) \n
		Defines the SPS interval. \n
			:param user_sps_int: S10| S20| S32| S40| S64| S80| S128| S160| S320| S640
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(user_sps_int, enums.SpsInt)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:SPS:SINTerval {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.SpsInt:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SINTerval \n
		Snippet: value: enums.SpsInt = driver.source.bb.eutra.downlink.user.sps.sinterval.get(userIx = repcap.UserIx.Default) \n
		Defines the SPS interval. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: user_sps_int: S10| S20| S32| S40| S64| S80| S128| S160| S320| S640"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:SPS:SINTerval?')
		return Conversions.str_to_scalar_enum(response, enums.SpsInt)
