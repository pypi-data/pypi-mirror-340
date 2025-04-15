from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UnscaledCls:
	"""Unscaled commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("unscaled", core, parent)

	def set(self, crs: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS:NMESsage:CNAV:EPHemeris:CRS:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.qzss.nmessage.cnav.ephemeris.crs.unscaled.set(crs = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the sine difference of orbital radius. \n
			:param crs: integer
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(crs)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:QZSS:NMESsage:CNAV:EPHemeris:CRS:UNSCaled {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS:NMESsage:CNAV:EPHemeris:CRS:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.qzss.nmessage.cnav.ephemeris.crs.unscaled.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the sine difference of orbital radius. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: crs: integer"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:QZSS:NMESsage:CNAV:EPHemeris:CRS:UNSCaled?')
		return Conversions.str_to_float(response)
