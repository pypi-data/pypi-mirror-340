from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SoffsetCls:
	"""Soffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("soffset", core, parent)

	def set(self, soffset: int, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:SOFFset \n
		Snippet: driver.source.bb.w3Gpp.mstation.pcpch.timing.soffset.set(soffset = 1, mobileStation = repcap.MobileStation.Default) \n
		This command defines the start offset of the PCPCH in access slots. The starting time delay in timeslots is calculated
		according to: 2 x Start Offset. \n
			:param soffset: integer Range: 1 to 14
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
		"""
		param = Conversions.decimal_value_to_str(soffset)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PCPCh:TIMing:SOFFset {param}')

	def get(self, mobileStation=repcap.MobileStation.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:SOFFset \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.pcpch.timing.soffset.get(mobileStation = repcap.MobileStation.Default) \n
		This command defines the start offset of the PCPCH in access slots. The starting time delay in timeslots is calculated
		according to: 2 x Start Offset. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: soffset: integer Range: 1 to 14"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PCPCh:TIMing:SOFFset?')
		return Conversions.str_to_int(response)
