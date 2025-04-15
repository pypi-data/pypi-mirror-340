from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CommentCls:
	"""Comment commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comment", core, parent)

	def get(self, sequencer=repcap.Sequencer.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:PLAYback:[SEQuencer<ST>]:COMMent \n
		Snippet: value: str = driver.source.bb.esequencer.playback.sequencer.comment.get(sequencer = repcap.Sequencer.Default) \n
		Displays comment information of the loaded file. \n
			:param sequencer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sequencer')
			:return: comment: string"""
		sequencer_cmd_val = self._cmd_group.get_repcap_cmd_value(sequencer, repcap.Sequencer)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:PLAYback:SEQuencer{sequencer_cmd_val}:COMMent?')
		return trim_str_response(response)
