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

	def set(self, pattern: str, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:SIGNal:L5Band:EL5S<US>:DATA:NMESsage:PATTern \n
		Snippet: driver.source.bb.gnss.svid.sbas.signal.l5Band.el5S.data.nmessage.pattern.set(pattern = rawAbc, satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Sets a bit pattern as data source. \n
			:param pattern: 64 bits
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'El5S')
		"""
		param = Conversions.value_to_str(pattern)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:SIGNal:L5Band:EL5S{index_cmd_val}:DATA:NMESsage:PATTern {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:SIGNal:L5Band:EL5S<US>:DATA:NMESsage:PATTern \n
		Snippet: value: str = driver.source.bb.gnss.svid.sbas.signal.l5Band.el5S.data.nmessage.pattern.get(satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Sets a bit pattern as data source. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'El5S')
			:return: pattern: 64 bits"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:SIGNal:L5Band:EL5S{index_cmd_val}:DATA:NMESsage:PATTern?')
		return trim_str_response(response)
