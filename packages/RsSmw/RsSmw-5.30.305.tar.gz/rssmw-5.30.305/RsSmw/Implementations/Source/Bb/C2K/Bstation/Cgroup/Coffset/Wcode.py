from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WcodeCls:
	"""Wcode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wcode", core, parent)

	def set(self, wcode: int, baseStation=repcap.BaseStation.Default, groupNull=repcap.GroupNull.Default, offset=repcap.Offset.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI0>:COFFset<CH>:WCODe \n
		Snippet: driver.source.bb.c2K.bstation.cgroup.coffset.wcode.set(wcode = 1, baseStation = repcap.BaseStation.Default, groupNull = repcap.GroupNull.Default, offset = repcap.Offset.Default) \n
		Assigns the Walsh Code to the channel. The standard assigns a fixed walsh code to some channels (F-PICH, for example,
		always uses Walsh code 0) . Generally, the Walsh code can only be varied within the range specified by the standard. For
		the traffic channels, this value is specific for the selected radio configuration. The value range of the Walsh code
		depends on the frame length, the channel coding type and the data rate. If one of these parameters is changed so that the
		set Walsh code gets invalid, the next permissible value is automatically set. \n
			:param wcode: integer Range: 0 to 255
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param offset: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
		"""
		param = Conversions.decimal_value_to_str(wcode)
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		offset_cmd_val = self._cmd_group.get_repcap_cmd_value(offset, repcap.Offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{baseStation_cmd_val}:CGRoup{groupNull_cmd_val}:COFFset{offset_cmd_val}:WCODe {param}')

	def get(self, baseStation=repcap.BaseStation.Default, groupNull=repcap.GroupNull.Default, offset=repcap.Offset.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI0>:COFFset<CH>:WCODe \n
		Snippet: value: int = driver.source.bb.c2K.bstation.cgroup.coffset.wcode.get(baseStation = repcap.BaseStation.Default, groupNull = repcap.GroupNull.Default, offset = repcap.Offset.Default) \n
		Assigns the Walsh Code to the channel. The standard assigns a fixed walsh code to some channels (F-PICH, for example,
		always uses Walsh code 0) . Generally, the Walsh code can only be varied within the range specified by the standard. For
		the traffic channels, this value is specific for the selected radio configuration. The value range of the Walsh code
		depends on the frame length, the channel coding type and the data rate. If one of these parameters is changed so that the
		set Walsh code gets invalid, the next permissible value is automatically set. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param offset: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: wcode: integer Range: 0 to 255"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		offset_cmd_val = self._cmd_group.get_repcap_cmd_value(offset, repcap.Offset)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{baseStation_cmd_val}:CGRoup{groupNull_cmd_val}:COFFset{offset_cmd_val}:WCODe?')
		return Conversions.str_to_int(response)
