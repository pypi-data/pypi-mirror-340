from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValueCls:
	"""Value commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("value", core, parent)

	def set(self, profile_value: float, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic:PRERrors:PROFile<GR>:VALue \n
		Snippet: driver.source.bb.gnss.svid.navic.prErrors.profile.value.set(profile_value = 1.0, satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Sets the pseudorange error value. \n
			:param profile_value: float Range: -100000 to 100000
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')
		"""
		param = Conversions.decimal_value_to_str(profile_value)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:NAVic:PRERrors:PROFile{index_cmd_val}:VALue {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic:PRERrors:PROFile<GR>:VALue \n
		Snippet: value: float = driver.source.bb.gnss.svid.navic.prErrors.profile.value.get(satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Sets the pseudorange error value. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')
			:return: profile_value: float Range: -100000 to 100000"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:NAVic:PRERrors:PROFile{index_cmd_val}:VALue?')
		return Conversions.str_to_float(response)
