from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StResetCls:
	"""StReset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stReset", core, parent)

	def set(self, sequencer=repcap.Sequencer.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:[SEQuencer<ST>]:STReam:STReset \n
		Snippet: driver.source.bb.esequencer.rtci.sequencer.stream.stReset.set(sequencer = repcap.Sequencer.Default) \n
		Reset system time in streaming interface, buffer is also empty in the coder board. Note: Do not use this command if
		streams are added in the 'I/Q Stream Mapper', for example if stream A and stream B are both routed to RF A. \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
		"""
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:RTCI:SEQuencer{sequencer_cmd_val}:STReam:STReset')

	def set_with_opc(self, sequencer=repcap.Sequencer.Default, opc_timeout_ms: int = -1) -> None:
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:RTCI:[SEQuencer<ST>]:STReam:STReset \n
		Snippet: driver.source.bb.esequencer.rtci.sequencer.stream.stReset.set_with_opc(sequencer = repcap.Sequencer.Default) \n
		Reset system time in streaming interface, buffer is also empty in the coder board. Note: Do not use this command if
		streams are added in the 'I/Q Stream Mapper', for example if stream A and stream B are both routed to RF A. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ESEQuencer:RTCI:SEQuencer{sequencer_cmd_val}:STReam:STReset', opc_timeout_ms)
