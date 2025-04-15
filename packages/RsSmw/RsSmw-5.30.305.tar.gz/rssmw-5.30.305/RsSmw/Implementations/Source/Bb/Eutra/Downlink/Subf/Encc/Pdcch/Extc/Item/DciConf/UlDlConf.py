from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............Internal.Utilities import trim_str_response
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlDlConfCls:
	"""UlDlConf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ulDlConf", core, parent)

	def set(self, dci_ul_dl_conf: str, subframeNull=repcap.SubframeNull.Default, itemNull=repcap.ItemNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:ITEM<CH0>:DCIConf:ULDLconf \n
		Snippet: driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.item.dciConf.ulDlConf.set(dci_ul_dl_conf = rawAbc, subframeNull = repcap.SubframeNull.Default, itemNull = repcap.ItemNull.Default) \n
		Sets the UL/DL configuration numbers. Each UL/DL configuration number consists of 3 bits and indicates one of the
		configurations listed in Figure 'Uplink-downlink configurations'. \n
			:param dci_ul_dl_conf: 64 bits
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param itemNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Item')
		"""
		param = Conversions.value_to_str(dci_ul_dl_conf)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		itemNull_cmd_val = self._cmd_group.get_repcap_cmd_value(itemNull, repcap.ItemNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:ITEM{itemNull_cmd_val}:DCIConf:ULDLconf {param}')

	def get(self, subframeNull=repcap.SubframeNull.Default, itemNull=repcap.ItemNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:ITEM<CH0>:DCIConf:ULDLconf \n
		Snippet: value: str = driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.item.dciConf.ulDlConf.get(subframeNull = repcap.SubframeNull.Default, itemNull = repcap.ItemNull.Default) \n
		Sets the UL/DL configuration numbers. Each UL/DL configuration number consists of 3 bits and indicates one of the
		configurations listed in Figure 'Uplink-downlink configurations'. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param itemNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Item')
			:return: dci_ul_dl_conf: 64 bits"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		itemNull_cmd_val = self._cmd_group.get_repcap_cmd_value(itemNull, repcap.ItemNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:ITEM{itemNull_cmd_val}:DCIConf:ULDLconf?')
		return trim_str_response(response)
