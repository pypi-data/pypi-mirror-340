from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ArbLenCls:
	"""ArbLen commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arbLen", core, parent)

	def get(self, userIx=repcap.UserIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:ARBLen \n
		Snippet: value: int = driver.source.bb.eutra.downlink.user.asPy.arbLen.get(userIx = repcap.UserIx.Default) \n
		Queries the suggested ARB sequence length. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: sug_arb_len: integer Range: 1 to 1E4"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:ARBLen?')
		return Conversions.str_to_int(response)
