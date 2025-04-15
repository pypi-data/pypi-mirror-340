from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AppendCls:
	"""Append commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("append", core, parent)

	def set(self, subframeNull=repcap.SubframeNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:[SUBF<ST0>]:ENCC:XPDCch:EXTC:APPend \n
		Snippet: driver.source.bb.v5G.downlink.subf.encc.xpdcch.extc.append.set(subframeNull = repcap.SubframeNull.Default) \n
		Adds a new row at the end of the DCI table. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
		"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:SUBF{subframeNull_cmd_val}:ENCC:XPDCch:EXTC:APPend')

	def set_with_opc(self, subframeNull=repcap.SubframeNull.Default, opc_timeout_ms: int = -1) -> None:
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:[SUBF<ST0>]:ENCC:XPDCch:EXTC:APPend \n
		Snippet: driver.source.bb.v5G.downlink.subf.encc.xpdcch.extc.append.set_with_opc(subframeNull = repcap.SubframeNull.Default) \n
		Adds a new row at the end of the DCI table. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:V5G:DL:SUBF{subframeNull_cmd_val}:ENCC:XPDCch:EXTC:APPend', opc_timeout_ms)
