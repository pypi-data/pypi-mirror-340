from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, profile_offset: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:PRERrors:PROFile:OFFSet \n
		Snippet: driver.source.bb.gnss.svid.galileo.prErrors.profile.offset.set(profile_offset = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Adds a start time offset. \n
			:param profile_offset: float Range: 0 to 86400
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(profile_offset)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:PRERrors:PROFile:OFFSet {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:PRERrors:PROFile:OFFSet \n
		Snippet: value: float = driver.source.bb.gnss.svid.galileo.prErrors.profile.offset.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Adds a start time offset. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: profile_offset: float Range: 0 to 86400"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:PRERrors:PROFile:OFFSet?')
		return Conversions.str_to_float(response)
