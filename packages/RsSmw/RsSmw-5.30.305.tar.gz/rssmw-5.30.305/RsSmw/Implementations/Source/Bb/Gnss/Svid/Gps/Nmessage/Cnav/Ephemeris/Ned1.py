from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ned1Cls:
	"""Ned1 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ned1", core, parent)

	def set(self, ned_1: int, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:NMESsage:CNAV:EPHemeris:NED1 \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.ned1.set(ned_1 = 1, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the NED accuracy index (NED0) , accuracy change indexs (NED1) and accuracy change rate index (NED2) . \n
			:param ned_1: integer Range: 0 to 7
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(ned_1)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:NMESsage:CNAV:EPHemeris:NED1 {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:NMESsage:CNAV:EPHemeris:NED1 \n
		Snippet: value: int = driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.ned1.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the NED accuracy index (NED0) , accuracy change indexs (NED1) and accuracy change rate index (NED2) . \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: ned_1: No help available"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:NMESsage:CNAV:EPHemeris:NED1?')
		return Conversions.str_to_int(response)
