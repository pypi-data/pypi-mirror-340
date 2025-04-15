from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DirectionCls:
	"""Direction commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("direction", core, parent)

	def set(self, direction: enums.ConnDirection, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce]:INPut:USER<CH>:DIRection \n
		Snippet: driver.source.inputPy.user.direction.set(direction = enums.ConnDirection.INPut, userIx = repcap.UserIx.Default) \n
		Sets the direction of the signal at the connector that can be an input or an output. \n
			:param direction: INPut| OUTPut| UNUSed INPut|OUTPut Input signal or output signal UNUSed No signals present at the connector.
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.ConnDirection)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce:INPut:USER{userIx_cmd_val}:DIRection {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.ConnDirection:
		"""SCPI: [SOURce]:INPut:USER<CH>:DIRection \n
		Snippet: value: enums.ConnDirection = driver.source.inputPy.user.direction.get(userIx = repcap.UserIx.Default) \n
		Sets the direction of the signal at the connector that can be an input or an output. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: direction: INPut| OUTPut| UNUSed INPut|OUTPut Input signal or output signal UNUSed No signals present at the connector."""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce:INPut:USER{userIx_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.ConnDirection)
