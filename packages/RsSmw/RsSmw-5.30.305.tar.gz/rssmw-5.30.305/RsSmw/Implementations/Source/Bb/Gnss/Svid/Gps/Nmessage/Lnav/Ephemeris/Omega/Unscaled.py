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

	def set(self, omega: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:NMESsage:LNAV:EPHemeris:OMEGa:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.lnav.ephemeris.omega.unscaled.set(omega = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the argument of perigee. \n
			:param omega: integer
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(omega)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:NMESsage:LNAV:EPHemeris:OMEGa:UNSCaled {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:NMESsage:LNAV:EPHemeris:OMEGa:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.gps.nmessage.lnav.ephemeris.omega.unscaled.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the argument of perigee. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: omega: integer"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:NMESsage:LNAV:EPHemeris:OMEGa:UNSCaled?')
		return Conversions.str_to_float(response)
