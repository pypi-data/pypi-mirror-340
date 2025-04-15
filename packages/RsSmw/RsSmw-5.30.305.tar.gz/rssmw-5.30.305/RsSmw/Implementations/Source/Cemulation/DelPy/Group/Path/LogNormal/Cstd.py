from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CstdCls:
	"""Cstd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cstd", core, parent)

	def set(self, cstd: int, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:DEL:GROup<ST>:PATH<CH>:LOGNormal:CSTD \n
		Snippet: driver.source.cemulation.delPy.group.path.logNormal.cstd.set(cstd = 1, fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param cstd: No help available
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.decimal_value_to_str(cstd)
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:DEL:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:LOGNormal:CSTD {param}')

	def get(self, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> int:
		"""SCPI: [SOURce<HW>]:CEMulation:DEL:GROup<ST>:PATH<CH>:LOGNormal:CSTD \n
		Snippet: value: int = driver.source.cemulation.delPy.group.path.logNormal.cstd.get(fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		No command help available \n
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: cstd: No help available"""
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:DEL:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:LOGNormal:CSTD?')
		return Conversions.str_to_int(response)
