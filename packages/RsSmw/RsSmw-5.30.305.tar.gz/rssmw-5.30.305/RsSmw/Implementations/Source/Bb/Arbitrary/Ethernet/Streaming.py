from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StreamingCls:
	"""Streaming commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("streaming", core, parent)

	def get_status(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:ETHernet:[STReaming]:STATus \n
		Snippet: value: str = driver.source.bb.arbitrary.ethernet.streaming.get_status() \n
		No command help available \n
			:return: status: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:ETHernet:STReaming:STATus?')
		return trim_str_response(response)
