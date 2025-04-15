from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PopCqiCls:
	"""PopCqi commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("popCqi", core, parent)

	def set(self, pop_cqi: float, mobileStation=repcap.MobileStation.Default, rowNull=repcap.RowNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH0>:POPCqi \n
		Snippet: driver.source.bb.w3Gpp.mstation.dpcch.hs.row.popCqi.set(pop_cqi = 1.0, mobileStation = repcap.MobileStation.Default, rowNull = repcap.RowNull.Default) \n
		(Release 8 and Later) Sets the power offset Poff_PCI/CQI of all PCI/CQI slots during the corresponding specified PCI/CQI
		From/To range relative to the [:SOURce<hw>]:BB:W3GPp:MSTation<st>:DPCCh:HS:POWer. \n
			:param pop_cqi: float Range: -10 to 10
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
		"""
		param = Conversions.decimal_value_to_str(pop_cqi)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:DPCCh:HS:ROW{rowNull_cmd_val}:POPCqi {param}')

	def get(self, mobileStation=repcap.MobileStation.Default, rowNull=repcap.RowNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH0>:POPCqi \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.dpcch.hs.row.popCqi.get(mobileStation = repcap.MobileStation.Default, rowNull = repcap.RowNull.Default) \n
		(Release 8 and Later) Sets the power offset Poff_PCI/CQI of all PCI/CQI slots during the corresponding specified PCI/CQI
		From/To range relative to the [:SOURce<hw>]:BB:W3GPp:MSTation<st>:DPCCh:HS:POWer. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: pop_cqi: float Range: -10 to 10"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:DPCCh:HS:ROW{rowNull_cmd_val}:POPCqi?')
		return Conversions.str_to_float(response)
