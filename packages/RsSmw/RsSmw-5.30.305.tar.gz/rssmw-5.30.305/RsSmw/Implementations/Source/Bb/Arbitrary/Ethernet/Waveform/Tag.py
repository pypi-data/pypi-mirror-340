from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TagCls:
	"""Tag commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tag", core, parent)

	def get(self, tag_name: str) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:WAVeform:TAG \n
		Snippet: value: str = driver.source.bb.arbitrary.ethernet.waveform.tag.get(tag_name = 'abc') \n
		Queries waveform tags defined in the waveform file with extension *.wv. Query results are returned in a comma-separated
		list. Listed are pairs '<TagName>'<'<TagValue>'> for each tag. \n
			:param tag_name: string Name of the waveform tag.
			:return: tag_value: string Value of the waveform tag."""
		param = Conversions.value_to_quoted_str(tag_name)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:ETHernet:WAVeform:TAG? {param}')
		return trim_str_response(response)
