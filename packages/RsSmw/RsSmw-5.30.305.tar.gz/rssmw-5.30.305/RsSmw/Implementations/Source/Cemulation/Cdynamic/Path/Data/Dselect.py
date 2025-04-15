from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DselectCls:
	"""Dselect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dselect", core, parent)

	def set(self, filename: str, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:DATA:DSELect \n
		Snippet: driver.source.cemulation.cdynamic.path.data.dselect.set(filename = 'abc', path = repcap.Path.Default) \n
		No command help available \n
			:param filename: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.value_to_quoted_str(filename)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:DATA:DSELect {param}')

	def get(self, path=repcap.Path.Default) -> str:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:DATA:DSELect \n
		Snippet: value: str = driver.source.cemulation.cdynamic.path.data.dselect.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: filename: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:DATA:DSELect?')
		return trim_str_response(response)
