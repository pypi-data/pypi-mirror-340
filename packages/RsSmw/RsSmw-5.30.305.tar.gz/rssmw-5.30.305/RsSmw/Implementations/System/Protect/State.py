from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, key: int = None, level=repcap.Level.Default) -> None:
		"""SCPI: SYSTem:PROTect<CH>:[STATe] \n
		Snippet: driver.system.protect.state.set(state = False, key = 1, level = repcap.Level.Default) \n
		Activates and deactivates the specified protection level. \n
			:param state: 1| ON| 0| OFF
			:param key: integer The respective functions are disabled when the protection level is activated. No password is required for activation of a level. A password must be entered to deactivate the protection level. The default password for the first level is 123456. This protection level is required to unlock internal adjustments for example.
			:param level: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Protect')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('state', state, DataType.Boolean), ArgSingle('key', key, DataType.Integer, None, is_optional=True))
		level_cmd_val = self._cmd_group.get_repcap_cmd_value(level, repcap.Level)
		self._core.io.write(f'SYSTem:PROTect{level_cmd_val}:STATe {param}'.rstrip())

	def get(self, level=repcap.Level.Default) -> bool:
		"""SCPI: SYSTem:PROTect<CH>:[STATe] \n
		Snippet: value: bool = driver.system.protect.state.get(level = repcap.Level.Default) \n
		Activates and deactivates the specified protection level. \n
			:param level: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Protect')
			:return: state: 1| ON| 0| OFF"""
		level_cmd_val = self._cmd_group.get_repcap_cmd_value(level, repcap.Level)
		response = self._core.io.query_str(f'SYSTem:PROTect{level_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
