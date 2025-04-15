from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AppendCls:
	"""Append commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("append", core, parent)

	def set(self, waveform: str, sequencer=repcap.Sequencer.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:[SEQuencer<ST>]:WLISt:SEGMent:APPend \n
		Snippet: driver.source.bb.esequencer.rtci.sequencer.wlist.segment.append.set(waveform = 'abc', sequencer = repcap.Sequencer.Default) \n
		Appends the specified waveform to the selected waveform list. \n
			:param waveform: string
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
		"""
		param = Conversions.value_to_quoted_str(waveform)
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:RTCI:SEQuencer{sequencer_cmd_val}:WLISt:SEGMent:APPend {param}')
