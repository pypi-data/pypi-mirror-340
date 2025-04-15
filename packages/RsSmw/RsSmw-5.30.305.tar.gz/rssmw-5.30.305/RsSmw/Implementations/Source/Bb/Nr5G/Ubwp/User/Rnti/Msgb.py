from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsgbCls:
	"""Msgb commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msgb", core, parent)

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:RNTI:MSGB \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.rnti.msgb.get(userNull = repcap.UserNull.Default) \n
		Sets the MsgB-RNTI of the user. It is a unique UE identification used as an identifier of the RRC connection and for
		scheduling with a temporary cell. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: msg_br_nti: integer Range: 1 to 65519"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:RNTI:MSGB?')
		return Conversions.str_to_int(response)
