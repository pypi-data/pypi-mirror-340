from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, baseStation=repcap.BaseStation.Default, groupNull=repcap.GroupNull.Default, offset=repcap.Offset.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI0>:COFFset<CH>:STATe \n
		Snippet: driver.source.bb.c2K.bstation.cgroup.coffset.state.set(state = False, baseStation = repcap.BaseStation.Default, groupNull = repcap.GroupNull.Default, offset = repcap.Offset.Default) \n
		This command activates/deactivates the selected channel. For the traffic channels, this value is specific for the
		selected radio configuration. \n
			:param state: 1| ON| 0| OFF
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param offset: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
		"""
		param = Conversions.bool_to_str(state)
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		offset_cmd_val = self._cmd_group.get_repcap_cmd_value(offset, repcap.Offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{baseStation_cmd_val}:CGRoup{groupNull_cmd_val}:COFFset{offset_cmd_val}:STATe {param}')

	def get(self, baseStation=repcap.BaseStation.Default, groupNull=repcap.GroupNull.Default, offset=repcap.Offset.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI0>:COFFset<CH>:STATe \n
		Snippet: value: bool = driver.source.bb.c2K.bstation.cgroup.coffset.state.get(baseStation = repcap.BaseStation.Default, groupNull = repcap.GroupNull.Default, offset = repcap.Offset.Default) \n
		This command activates/deactivates the selected channel. For the traffic channels, this value is specific for the
		selected radio configuration. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param offset: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: state: 1| ON| 0| OFF"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		offset_cmd_val = self._cmd_group.get_repcap_cmd_value(offset, repcap.Offset)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{baseStation_cmd_val}:CGRoup{groupNull_cmd_val}:COFFset{offset_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
