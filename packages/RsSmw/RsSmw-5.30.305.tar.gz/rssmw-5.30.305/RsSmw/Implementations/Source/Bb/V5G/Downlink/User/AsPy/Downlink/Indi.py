from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IndiCls:
	"""Indi commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("indi", core, parent)

	def set(self, starting_ndi: bool, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:DL:INDI \n
		Snippet: driver.source.bb.v5G.downlink.user.asPy.downlink.indi.set(starting_ndi = False, userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param starting_ndi: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(starting_ndi)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:DL:INDI {param}')

	def get(self, userIx=repcap.UserIx.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:AS:DL:INDI \n
		Snippet: value: bool = driver.source.bb.v5G.downlink.user.asPy.downlink.indi.get(userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: starting_ndi: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:AS:DL:INDI?')
		return Conversions.str_to_bool(response)
