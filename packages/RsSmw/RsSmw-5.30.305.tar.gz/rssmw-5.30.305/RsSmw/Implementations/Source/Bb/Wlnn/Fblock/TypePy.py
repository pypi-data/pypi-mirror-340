from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.WlannFbType, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:TYPE \n
		Snippet: driver.source.bb.wlnn.fblock.typePy.set(type_py = enums.WlannFbType.BEACon, frameBlock = repcap.FrameBlock.Default) \n
		The command selects the PPDU type. \n
			:param type_py: DATA| SOUNding| BEACon| TRIGger DATA Only Data Long Training Fields are used to probe the channel. SOUNding Staggered preambles are used to probe additional dimension of the MIMO channel. Only Physical Layer Mode GREEN FIELD is available. BEACon Frame type 'Beacon' is used to probe the channel.
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.WlannFbType)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default) -> enums.WlannFbType:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:TYPE \n
		Snippet: value: enums.WlannFbType = driver.source.bb.wlnn.fblock.typePy.get(frameBlock = repcap.FrameBlock.Default) \n
		The command selects the PPDU type. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: type_py: DATA| SOUNding| BEACon| TRIGger DATA Only Data Long Training Fields are used to probe the channel. SOUNding Staggered preambles are used to probe additional dimension of the MIMO channel. Only Physical Layer Mode GREEN FIELD is available. BEACon Frame type 'Beacon' is used to probe the channel."""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbType)
