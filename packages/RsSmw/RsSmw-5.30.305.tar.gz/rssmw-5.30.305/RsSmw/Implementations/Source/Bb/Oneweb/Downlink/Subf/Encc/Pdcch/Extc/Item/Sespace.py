from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SespaceCls:
	"""Sespace commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sespace", core, parent)

	def set(self, search_space: enums.OneWebSearchSpace, subframeNull=repcap.SubframeNull.Default, itemNull=repcap.ItemNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:ITEM<CH0>:SESPace \n
		Snippet: driver.source.bb.oneweb.downlink.subf.encc.pdcch.extc.item.sespace.set(search_space = enums.OneWebSearchSpace._1, subframeNull = repcap.SubframeNull.Default, itemNull = repcap.ItemNull.Default) \n
		If enabled, this parameter configures the PDCCH DCI to be transmitted within the common or UE-specific search space. \n
			:param search_space: AUTO| COMMon| UE| ON| 1 COMMon|UE Common and UE-specific search spaces, as defined in the 3GPP specification OFF|AUTO For backwards compatibility only.
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param itemNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Item')
		"""
		param = Conversions.enum_scalar_to_str(search_space, enums.OneWebSearchSpace)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		itemNull_cmd_val = self._cmd_group.get_repcap_cmd_value(itemNull, repcap.ItemNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:ITEM{itemNull_cmd_val}:SESPace {param}')

	# noinspection PyTypeChecker
	def get(self, subframeNull=repcap.SubframeNull.Default, itemNull=repcap.ItemNull.Default) -> enums.OneWebSearchSpace:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:ITEM<CH0>:SESPace \n
		Snippet: value: enums.OneWebSearchSpace = driver.source.bb.oneweb.downlink.subf.encc.pdcch.extc.item.sespace.get(subframeNull = repcap.SubframeNull.Default, itemNull = repcap.ItemNull.Default) \n
		If enabled, this parameter configures the PDCCH DCI to be transmitted within the common or UE-specific search space. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param itemNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Item')
			:return: search_space: AUTO| COMMon| UE| ON| 1 COMMon|UE Common and UE-specific search spaces, as defined in the 3GPP specification OFF|AUTO For backwards compatibility only."""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		itemNull_cmd_val = self._cmd_group.get_repcap_cmd_value(itemNull, repcap.ItemNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ONEWeb:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:ITEM{itemNull_cmd_val}:SESPace?')
		return Conversions.str_to_scalar_enum(response, enums.OneWebSearchSpace)
