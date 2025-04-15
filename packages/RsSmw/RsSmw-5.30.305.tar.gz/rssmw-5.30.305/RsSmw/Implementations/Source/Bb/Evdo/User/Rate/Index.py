from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IndexCls:
	"""Index commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("index", core, parent)

	def set(self, index: int, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:USER<ST>:RATE:INDex \n
		Snippet: driver.source.bb.evdo.user.rate.index.set(index = 1, userIx = repcap.UserIx.Default) \n
		Determines the rate index. Note: Selected rate becomes effective at the beginning of the next packet transmitted to the
		selected user. \n
			:param index: integer Range: 1 to 12 (physical layer subtype 0&1) , 1 to 14 (physical layer subtype 2) , 1 to 28 (physical layer subtype 3)
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(index)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{userIx_cmd_val}:RATE:INDex {param}')

	def get(self, userIx=repcap.UserIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EVDO:USER<ST>:RATE:INDex \n
		Snippet: value: int = driver.source.bb.evdo.user.rate.index.get(userIx = repcap.UserIx.Default) \n
		Determines the rate index. Note: Selected rate becomes effective at the beginning of the next packet transmitted to the
		selected user. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: index: integer Range: 1 to 12 (physical layer subtype 0&1) , 1 to 14 (physical layer subtype 2) , 1 to 28 (physical layer subtype 3)"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{userIx_cmd_val}:RATE:INDex?')
		return Conversions.str_to_int(response)
