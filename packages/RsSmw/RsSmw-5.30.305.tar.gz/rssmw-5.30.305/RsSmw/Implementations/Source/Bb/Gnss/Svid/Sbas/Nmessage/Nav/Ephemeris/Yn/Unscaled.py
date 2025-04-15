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

	def set(self, yn: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:NMESsage:NAV:EPHemeris:YN:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.sbas.nmessage.nav.ephemeris.yn.unscaled.set(yn = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the Xn, Yn and Zn coordinates in PZ-90. \n
			:param yn: integer
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(yn)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:NMESsage:NAV:EPHemeris:YN:UNSCaled {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:NMESsage:NAV:EPHemeris:YN:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.sbas.nmessage.nav.ephemeris.yn.unscaled.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the Xn, Yn and Zn coordinates in PZ-90. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: yn: No help available"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:NMESsage:NAV:EPHemeris:YN:UNSCaled?')
		return Conversions.str_to_float(response)
