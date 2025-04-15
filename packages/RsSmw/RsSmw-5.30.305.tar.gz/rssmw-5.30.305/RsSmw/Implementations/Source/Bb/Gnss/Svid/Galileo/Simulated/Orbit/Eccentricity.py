from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EccentricityCls:
	"""Eccentricity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eccentricity", core, parent)

	def set(self, eccentricity: int, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:SIMulated:ORBit:ECCentricity \n
		Snippet: driver.source.bb.gnss.svid.galileo.simulated.orbit.eccentricity.set(eccentricity = 1, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the eccentricity. \n
			:param eccentricity: integer Range: 0 to 4294967295
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(eccentricity)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:SIMulated:ORBit:ECCentricity {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:SIMulated:ORBit:ECCentricity \n
		Snippet: value: int = driver.source.bb.gnss.svid.galileo.simulated.orbit.eccentricity.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the eccentricity. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: eccentricity: integer Range: 0 to 4294967295"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:SIMulated:ORBit:ECCentricity?')
		return Conversions.str_to_int(response)
