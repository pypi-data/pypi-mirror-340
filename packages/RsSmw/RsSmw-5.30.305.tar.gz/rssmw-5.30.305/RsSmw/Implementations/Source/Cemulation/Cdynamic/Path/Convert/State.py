from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, cdyn_convert_file: bool, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:CONVert:STATe \n
		Snippet: driver.source.cemulation.cdynamic.path.convert.state.set(cdyn_convert_file = False, path = repcap.Path.Default) \n
		No command help available \n
			:param cdyn_convert_file: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.bool_to_str(cdyn_convert_file)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:CONVert:STATe {param}')

	def get(self, path=repcap.Path.Default) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:CONVert:STATe \n
		Snippet: value: bool = driver.source.cemulation.cdynamic.path.convert.state.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: cdyn_convert_file: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:CONVert:STATe?')
		return Conversions.str_to_bool(response)
