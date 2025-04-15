from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:PATTern \n
		Snippet: driver.source.bb.v5G.downlink.user.pattern.set(pattern = rawAbc, userIx = repcap.UserIx.Default) \n
		Sets a bit pattern as data source. The command is relevant for: [:SOURce<hw>]:BB:V5G:DL:USER<ch>:DATAPATTern. \n
			:param pattern: 64 bit
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.value_to_str(pattern)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:PATTern {param}')

	def get(self, userIx=repcap.UserIx.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:PATTern \n
		Snippet: value: str = driver.source.bb.v5G.downlink.user.pattern.get(userIx = repcap.UserIx.Default) \n
		Sets a bit pattern as data source. The command is relevant for: [:SOURce<hw>]:BB:V5G:DL:USER<ch>:DATAPATTern. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: pattern: 64 bit"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:PATTern?')
		return trim_str_response(response)
