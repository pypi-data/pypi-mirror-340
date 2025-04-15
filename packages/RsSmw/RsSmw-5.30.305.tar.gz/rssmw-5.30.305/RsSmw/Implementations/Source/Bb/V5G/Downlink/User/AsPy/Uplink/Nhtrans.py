from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NhtransCls:
	"""Nhtrans commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nhtrans", core, parent)

	def set(self, num_harq_trans: int, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:UL:NHTRans \n
		Snippet: driver.source.bb.v5G.downlink.user.asPy.uplink.nhtrans.set(num_harq_trans = 1, userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param num_harq_trans: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(num_harq_trans)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:UL:NHTRans {param}')

	def get(self, userIx=repcap.UserIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:UL:NHTRans \n
		Snippet: value: int = driver.source.bb.v5G.downlink.user.asPy.uplink.nhtrans.get(userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: num_harq_trans: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:UL:NHTRans?')
		return Conversions.str_to_int(response)
