from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, location: str, baseSt=repcap.BaseSt.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:[SELect] \n
		Snippet: driver.source.bb.gnss.rtk.base.location.select.set(location = 'abc', baseSt = repcap.BaseSt.Default) \n
		Selects the geographic location of the RTK base station. \n
			:param location: string 'User Defined' Enables the definition of the 'Latitude', 'Longitude' and 'Altitude' of the GNSS receiver with fixed position in the ECEF WGS84 coordinate system. 'City' Selects one of the predefined geographic locations, see Table 'Coordinates of the simulated predefined positions'. The parameters latitude, longitude and altitude are set according to the selected position.
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
		"""
		param = Conversions.value_to_quoted_str(location)
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:SELect {param}')

	def get(self, baseSt=repcap.BaseSt.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:[SELect] \n
		Snippet: value: str = driver.source.bb.gnss.rtk.base.location.select.get(baseSt = repcap.BaseSt.Default) \n
		Selects the geographic location of the RTK base station. \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:return: location: string 'User Defined' Enables the definition of the 'Latitude', 'Longitude' and 'Altitude' of the GNSS receiver with fixed position in the ECEF WGS84 coordinate system. 'City' Selects one of the predefined geographic locations, see Table 'Coordinates of the simulated predefined positions'. The parameters latitude, longitude and altitude are set according to the selected position."""
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:SELect?')
		return trim_str_response(response)
