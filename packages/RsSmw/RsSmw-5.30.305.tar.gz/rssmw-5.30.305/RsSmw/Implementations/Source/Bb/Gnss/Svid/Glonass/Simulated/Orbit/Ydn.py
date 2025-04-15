from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class YdnCls:
	"""Ydn commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ydn", core, parent)

	def set(self, yn_dot: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIMulated:ORBit:YDN \n
		Snippet: driver.source.bb.gnss.svid.glonass.simulated.orbit.ydn.set(yn_dot = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the velocity components X'n, Y'n and Z'n. \n
			:param yn_dot: float
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(yn_dot)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIMulated:ORBit:YDN {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIMulated:ORBit:YDN \n
		Snippet: value: float = driver.source.bb.gnss.svid.glonass.simulated.orbit.ydn.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the velocity components X'n, Y'n and Z'n. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: yn_dot: No help available"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIMulated:ORBit:YDN?')
		return Conversions.str_to_float(response)
