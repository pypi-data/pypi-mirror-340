from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SvidCls:
	"""Svid commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("svid", core, parent)

	def set(self, svid: enums.Svid, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:XONA:PRERrors:COPY:SVID \n
		Snippet: driver.source.bb.gnss.svid.xona.prErrors.copy.svid.set(svid = enums.Svid._1, satelliteSvid = repcap.SatelliteSvid.Default) \n
		No command help available \n
			:param svid: No help available
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.enum_scalar_to_str(svid, enums.Svid)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:XONA:PRERrors:COPY:SVID {param}')

	# noinspection PyTypeChecker
	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> enums.Svid:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:XONA:PRERrors:COPY:SVID \n
		Snippet: value: enums.Svid = driver.source.bb.gnss.svid.xona.prErrors.copy.svid.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		No command help available \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: svid: No help available"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:XONA:PRERrors:COPY:SVID?')
		return Conversions.str_to_scalar_enum(response, enums.Svid)
