from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, pr_erors_mode: enums.PseudorangeMode, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:XONA:PRERrors:MODE \n
		Snippet: driver.source.bb.gnss.svid.xona.prErrors.mode.set(pr_erors_mode = enums.PseudorangeMode.CONStant, satelliteSvid = repcap.SatelliteSvid.Default) \n
		No command help available \n
			:param pr_erors_mode: No help available
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.enum_scalar_to_str(pr_erors_mode, enums.PseudorangeMode)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:XONA:PRERrors:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> enums.PseudorangeMode:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:XONA:PRERrors:MODE \n
		Snippet: value: enums.PseudorangeMode = driver.source.bb.gnss.svid.xona.prErrors.mode.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		No command help available \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: pr_erors_mode: No help available"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:XONA:PRERrors:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PseudorangeMode)
