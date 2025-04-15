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
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ESTReaming:WAVeform:TAG \n
		Snippet: value: str = driver.source.bb.esequencer.estreaming.waveform.tag.get(tag_name = 'abc') \n
		No command help available \n
			:param tag_name: No help available
			:return: tag_value: No help available"""
		param = Conversions.value_to_quoted_str(tag_name)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:ESTReaming:WAVeform:TAG? {param}')
		return trim_str_response(response)
