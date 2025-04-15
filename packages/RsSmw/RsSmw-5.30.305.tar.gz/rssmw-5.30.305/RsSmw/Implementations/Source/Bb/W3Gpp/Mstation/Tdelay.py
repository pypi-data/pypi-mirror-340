from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdelayCls:
	"""Tdelay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdelay", core, parent)

	def set(self, tdelay: int, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:TDELay \n
		Snippet: driver.source.bb.w3Gpp.mstation.tdelay.set(tdelay = 1, mobileStation = repcap.MobileStation.Default) \n
		Adds a time shift for the selected user equipment compared to user equipment 1. \n
			:param tdelay: integer Range: 0 to 38400, Unit: chip
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
		"""
		param = Conversions.decimal_value_to_str(tdelay)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:TDELay {param}')

	def get(self, mobileStation=repcap.MobileStation.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:TDELay \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.tdelay.get(mobileStation = repcap.MobileStation.Default) \n
		Adds a time shift for the selected user equipment compared to user equipment 1. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: tdelay: integer Range: 0 to 38400, Unit: chip"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:TDELay?')
		return Conversions.str_to_int(response)
