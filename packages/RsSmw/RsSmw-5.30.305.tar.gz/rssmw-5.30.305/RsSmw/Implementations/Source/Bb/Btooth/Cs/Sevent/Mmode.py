from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmodeCls:
	"""Mmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mmode", core, parent)

	def set(self, main_mode: enums.BtoCsMainMode, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MMODe \n
		Snippet: driver.source.bb.btooth.cs.sevent.mmode.set(main_mode = enums.BtoCsMainMode.MODE1, channelNull = repcap.ChannelNull.Default) \n
		Sets the main mode for the first subevent SEVent0. All following subevents use the same main mode. For an overview on
		available submodes per main mode, see Table 'CS step main modes and submodes'. \n
			:param main_mode: MODE1| MODE2| MODE3 MODE1 Mode-1 mode with no submode available. MODE2 Mode-2 mode with submodes Mode-1 and Mode-3 available. MODE3 Mode-3 mode with submodes Mode-1 and Mode-2 available.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(main_mode, enums.BtoCsMainMode)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MMODe {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsMainMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MMODe \n
		Snippet: value: enums.BtoCsMainMode = driver.source.bb.btooth.cs.sevent.mmode.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the main mode for the first subevent SEVent0. All following subevents use the same main mode. For an overview on
		available submodes per main mode, see Table 'CS step main modes and submodes'. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: main_mode: MODE1| MODE2| MODE3 MODE1 Mode-1 mode with no submode available. MODE2 Mode-2 mode with submodes Mode-1 and Mode-3 available. MODE3 Mode-3 mode with submodes Mode-1 and Mode-2 available."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsMainMode)
