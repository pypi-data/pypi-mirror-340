from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WrdReadCls:
	"""WrdRead commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wrdRead", core, parent)

	def get(self, sequencer=repcap.Sequencer.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ESTReaming:[SEQuencer<ST>]:STReam:WRDRead \n
		Snippet: value: float = driver.source.bb.esequencer.estreaming.sequencer.stream.wrdRead.get(sequencer = repcap.Sequencer.Default) \n
		No command help available \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
			:return: value: No help available"""
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:ESTReaming:SEQuencer{sequencer_cmd_val}:STReam:WRDRead?')
		return Conversions.str_to_float(response)
