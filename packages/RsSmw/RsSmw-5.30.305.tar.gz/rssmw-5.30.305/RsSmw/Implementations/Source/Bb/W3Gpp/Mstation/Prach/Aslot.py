from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AslotCls:
	"""Aslot commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aslot", core, parent)

	def set(self, aslot: int, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:ASLot \n
		Snippet: driver.source.bb.w3Gpp.mstation.prach.aslot.set(aslot = 1, mobileStation = repcap.MobileStation.Default) \n
		No command help available \n
			:param aslot: No help available
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
		"""
		param = Conversions.decimal_value_to_str(aslot)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PRACh:ASLot {param}')

	def get(self, mobileStation=repcap.MobileStation.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:ASLot \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.prach.aslot.get(mobileStation = repcap.MobileStation.Default) \n
		No command help available \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: aslot: No help available"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PRACh:ASLot?')
		return Conversions.str_to_int(response)
