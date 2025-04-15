from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PreambleCls:
	"""Preamble commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("preamble", core, parent)

	def get(self, mobileStation=repcap.MobileStation.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:DPOWer:PREamble \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.pcpch.timing.dpower.preamble.get(mobileStation = repcap.MobileStation.Default) \n
		Queries level correction value for the last AICH preamble before the message part. This value is identical to the
		correction value for the CD preamble. The level of the other preambles can be calculated by subtracting the set Preamble
		Power Step. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: preamble: float Range: -80 to 0"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PCPCh:TIMing:DPOWer:PREamble?')
		return Conversions.str_to_float(response)
