from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcodeCls:
	"""Ccode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccode", core, parent)

	def get(self, mobileStation=repcap.MobileStation.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:CCODe \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.dpcch.hs.ccode.get(mobileStation = repcap.MobileStation.Default) \n
		Queries the channelization code and the modulation branch of the HS-DPCCH. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: ccode: integer Range: 1 to 64"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:DPCCh:HS:CCODe?')
		return Conversions.str_to_int(response)
