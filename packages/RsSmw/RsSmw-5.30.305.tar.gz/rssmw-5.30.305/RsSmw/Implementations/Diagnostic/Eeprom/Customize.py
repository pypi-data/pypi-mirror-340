from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CustomizeCls:
	"""Customize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("customize", core, parent)

	def set(self, board: str, index: int, sub_board: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: DIAGnostic<HW>:EEPRom<CH>:CUSTomize \n
		Snippet: driver.diagnostic.eeprom.customize.set(board = 'abc', index = 1, sub_board = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param board: No help available
			:param index: No help available
			:param sub_board: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eeprom')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('board', board, DataType.String), ArgSingle('index', index, DataType.Integer), ArgSingle('sub_board', sub_board, DataType.Integer))
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'DIAGnostic<HwInstance>:EEPRom{channel_cmd_val}:CUSTomize {param}'.rstrip())
