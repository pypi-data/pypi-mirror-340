from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.Utilities import trim_str_response
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:DTX:PATTern \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.dtx.pattern.set(pattern = 'abc', mobileStation = repcap.MobileStation.Default) \n
		The command sets the user-definable bit pattern for the DTX. \n
			:param pattern: string
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
		"""
		param = Conversions.value_to_quoted_str(pattern)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:HSUPa:DPCCh:E:FRC:DTX:PATTern {param}')

	def get(self, mobileStation=repcap.MobileStation.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:DTX:PATTern \n
		Snippet: value: str = driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.dtx.pattern.get(mobileStation = repcap.MobileStation.Default) \n
		The command sets the user-definable bit pattern for the DTX. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: pattern: string"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:HSUPa:DPCCh:E:FRC:DTX:PATTern?')
		return trim_str_response(response)
