from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............Internal.Utilities import trim_str_response
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou:SIGNal:L1Band:B1I:DATA:NMESsage:PATTern \n
		Snippet: driver.source.bb.gnss.svid.beidou.signal.l1Band.b1I.data.nmessage.pattern.set(pattern = rawAbc, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets a bit pattern as data source. \n
			:param pattern: 64 bits
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.value_to_str(pattern)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:BEIDou:SIGNal:L1Band:B1I:DATA:NMESsage:PATTern {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou:SIGNal:L1Band:B1I:DATA:NMESsage:PATTern \n
		Snippet: value: str = driver.source.bb.gnss.svid.beidou.signal.l1Band.b1I.data.nmessage.pattern.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets a bit pattern as data source. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: pattern: 64 bits"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:BEIDou:SIGNal:L1Band:B1I:DATA:NMESsage:PATTern?')
		return trim_str_response(response)
