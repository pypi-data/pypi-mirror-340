from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, satelliteSvid=repcap.SatelliteSvid.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIGNal:L2Band:L2CDma<US0>:PILot:SCODe:[STATe] \n
		Snippet: driver.source.bb.gnss.svid.glonass.signal.l2Band.l2Cdma.pilot.scode.state.set(state = False, satelliteSvid = repcap.SatelliteSvid.Default, indexNull = repcap.IndexNull.Default) \n
		Activates the secondary code in the data/pilot channel. \n
			:param state: 1| ON| 0| OFF
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'L2Cdma')
		"""
		param = Conversions.bool_to_str(state)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIGNal:L2Band:L2CDma{indexNull_cmd_val}:PILot:SCODe:STATe {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default, indexNull=repcap.IndexNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIGNal:L2Band:L2CDma<US0>:PILot:SCODe:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.svid.glonass.signal.l2Band.l2Cdma.pilot.scode.state.get(satelliteSvid = repcap.SatelliteSvid.Default, indexNull = repcap.IndexNull.Default) \n
		Activates the secondary code in the data/pilot channel. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'L2Cdma')
			:return: state: 1| ON| 0| OFF"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIGNal:L2Band:L2CDma{indexNull_cmd_val}:PILot:SCODe:STATe?')
		return Conversions.str_to_bool(response)
