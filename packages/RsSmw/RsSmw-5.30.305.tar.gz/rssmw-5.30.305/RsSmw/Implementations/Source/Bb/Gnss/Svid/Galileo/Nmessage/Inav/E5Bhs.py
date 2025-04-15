from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E5BhsCls:
	"""E5Bhs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("e5Bhs", core, parent)

	def set(self, hs_e_5_b: int, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:NMESsage:INAV:E5BHS \n
		Snippet: driver.source.bb.gnss.svid.galileo.nmessage.inav.e5Bhs.set(hs_e_5_b = 1, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the signal health status - E5bHS parameter. \n
			:param hs_e_5_b: integer Range: -1 to 1
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(hs_e_5_b)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:NMESsage:INAV:E5BHS {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:NMESsage:INAV:E5BHS \n
		Snippet: value: int = driver.source.bb.gnss.svid.galileo.nmessage.inav.e5Bhs.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the signal health status - E5bHS parameter. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: hs_e_5_b: integer Range: -1 to 1"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:NMESsage:INAV:E5BHS?')
		return Conversions.str_to_int(response)
