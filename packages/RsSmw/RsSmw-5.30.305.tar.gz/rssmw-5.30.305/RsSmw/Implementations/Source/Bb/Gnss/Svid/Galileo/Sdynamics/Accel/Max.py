from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaxCls:
	"""Max commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("max", core, parent)

	def set(self, max_acceleration: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:SDYNamics:ACCel:MAX \n
		Snippet: driver.source.bb.gnss.svid.galileo.sdynamics.accel.max.set(max_acceleration = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the maximum acceleration. \n
			:param max_acceleration: float Range: 0.01 to 1000
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(max_acceleration)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:SDYNamics:ACCel:MAX {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:SDYNamics:ACCel:MAX \n
		Snippet: value: float = driver.source.bb.gnss.svid.galileo.sdynamics.accel.max.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the maximum acceleration. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: max_acceleration: float Range: 0.01 to 1000"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:SDYNamics:ACCel:MAX?')
		return Conversions.str_to_float(response)
