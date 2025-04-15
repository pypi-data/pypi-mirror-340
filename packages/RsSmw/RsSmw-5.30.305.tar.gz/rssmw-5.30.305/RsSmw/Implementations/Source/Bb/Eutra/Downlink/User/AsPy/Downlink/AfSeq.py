from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfSeqCls:
	"""AfSeq commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("afSeq", core, parent)

	def set(self, autofill_seq: bool, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:AFSeq \n
		Snippet: driver.source.bb.eutra.downlink.user.asPy.downlink.afSeq.set(autofill_seq = False, userIx = repcap.UserIx.Default) \n
		Enables the automatic configuration of the DCIs. \n
			:param autofill_seq: 1| ON| 0| OFF
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(autofill_seq)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:DL:AFSeq {param}')

	def get(self, userIx=repcap.UserIx.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:AFSeq \n
		Snippet: value: bool = driver.source.bb.eutra.downlink.user.asPy.downlink.afSeq.get(userIx = repcap.UserIx.Default) \n
		Enables the automatic configuration of the DCIs. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: autofill_seq: 1| ON| 0| OFF"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{userIx_cmd_val}:AS:DL:AFSeq?')
		return Conversions.str_to_bool(response)
