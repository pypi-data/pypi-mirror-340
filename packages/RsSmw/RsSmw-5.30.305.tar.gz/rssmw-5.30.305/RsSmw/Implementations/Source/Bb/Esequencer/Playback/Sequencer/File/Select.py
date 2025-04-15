from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, filename: str, sequencer=repcap.Sequencer.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:PLAYback:[SEQuencer<ST>]:FILE:[SELect] \n
		Snippet: driver.source.bb.esequencer.playback.sequencer.file.select.set(filename = 'abc', sequencer = repcap.Sequencer.Default) \n
		Accesses the standard 'File Select' function of the instrument to load a user written PDW file. The provided navigation
		possibilities in the dialog are self-explanatory. \n
			:param filename: string
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
		"""
		param = Conversions.value_to_quoted_str(filename)
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:PLAYback:SEQuencer{sequencer_cmd_val}:FILE:SELect {param}')

	def get(self, sequencer=repcap.Sequencer.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:PLAYback:[SEQuencer<ST>]:FILE:[SELect] \n
		Snippet: value: str = driver.source.bb.esequencer.playback.sequencer.file.select.get(sequencer = repcap.Sequencer.Default) \n
		Accesses the standard 'File Select' function of the instrument to load a user written PDW file. The provided navigation
		possibilities in the dialog are self-explanatory. \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
			:return: filename: string"""
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:PLAYback:SEQuencer{sequencer_cmd_val}:FILE:SELect?')
		return trim_str_response(response)
