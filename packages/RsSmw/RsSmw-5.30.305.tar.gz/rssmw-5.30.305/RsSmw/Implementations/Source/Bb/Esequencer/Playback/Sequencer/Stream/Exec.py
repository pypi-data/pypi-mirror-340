from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExecCls:
	"""Exec commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("exec", core, parent)

	def get(self, sequencer=repcap.Sequencer.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:PLAYback:[SEQuencer<ST>]:STReam:EXEC \n
		Snippet: value: float = driver.source.bb.esequencer.playback.sequencer.stream.exec.get(sequencer = repcap.Sequencer.Default) \n
		Queries data from streaming interface registers for system time and executed PDWs. \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
			:return: value: float"""
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:PLAYback:SEQuencer{sequencer_cmd_val}:STReam:EXEC?')
		return Conversions.str_to_float(response)
