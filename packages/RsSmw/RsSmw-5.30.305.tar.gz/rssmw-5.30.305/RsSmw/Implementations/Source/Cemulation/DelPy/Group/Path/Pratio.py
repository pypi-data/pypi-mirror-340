from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PratioCls:
	"""Pratio commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pratio", core, parent)

	def set(self, pratio: float, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:DEL:GROup<ST>:PATH<CH>:PRATio \n
		Snippet: driver.source.cemulation.delPy.group.path.pratio.set(pratio = 1.0, fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param pratio: No help available
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.decimal_value_to_str(pratio)
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:DEL:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:PRATio {param}')

	def get(self, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:DEL:GROup<ST>:PATH<CH>:PRATio \n
		Snippet: value: float = driver.source.cemulation.delPy.group.path.pratio.get(fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: pratio: No help available"""
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:DEL:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:PRATio?')
		return Conversions.str_to_float(response)
