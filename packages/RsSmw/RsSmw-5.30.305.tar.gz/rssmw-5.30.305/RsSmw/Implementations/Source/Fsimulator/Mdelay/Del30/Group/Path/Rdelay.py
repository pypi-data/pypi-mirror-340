from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdelayCls:
	"""Rdelay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rdelay", core, parent)

	def get(self, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:MDELay:DEL30:GROup<ST>:PATH<CH>:RDELay \n
		Snippet: value: float = driver.source.fsimulator.mdelay.del30.group.path.rdelay.get(fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		Queries the resulting delay of the paths for the selected fading configuration. The resulting delay is the sum of the
		basic delay and the additional delay that you set via the following commands:
		[:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:BDELay [:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:ADELay \n
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: rdelay: float Range: depends on the installed options* For example values, see also 'Narrowband and wideband fading characteristics'."""
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:MDELay:DEL30:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:RDELay?')
		return Conversions.str_to_float(response)
