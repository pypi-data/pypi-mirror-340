from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZnCls:
	"""Zn commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zn", core, parent)

	def set(self, zn: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:SIMulated:ORBit:ZN \n
		Snippet: driver.source.bb.gnss.svid.sbas.simulated.orbit.zn.set(zn = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Set the Xn, Yn and Zn coordinates in PZ-90. \n
			:param zn: float
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(zn)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:SIMulated:ORBit:ZN {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS:SIMulated:ORBit:ZN \n
		Snippet: value: float = driver.source.bb.gnss.svid.sbas.simulated.orbit.zn.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Set the Xn, Yn and Zn coordinates in PZ-90. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: zn: float"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:SBAS:SIMulated:ORBit:ZN?')
		return Conversions.str_to_float(response)
