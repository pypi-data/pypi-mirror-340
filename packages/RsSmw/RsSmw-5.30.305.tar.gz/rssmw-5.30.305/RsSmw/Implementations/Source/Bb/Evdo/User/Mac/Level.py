from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: float, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:USER<ST>:MAC:LEVel \n
		Snippet: driver.source.bb.evdo.user.mac.level.set(level = 1.0, userIx = repcap.UserIx.Default) \n
		Sets the power within the MAC channel that is dedicated to the selected user. \n
			:param level: float Range: -25 to -7
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(level)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{userIx_cmd_val}:MAC:LEVel {param}')

	def get(self, userIx=repcap.UserIx.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EVDO:USER<ST>:MAC:LEVel \n
		Snippet: value: float = driver.source.bb.evdo.user.mac.level.get(userIx = repcap.UserIx.Default) \n
		Sets the power within the MAC channel that is dedicated to the selected user. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: level: float Range: -25 to -7"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{userIx_cmd_val}:MAC:LEVel?')
		return Conversions.str_to_float(response)
