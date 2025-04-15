from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpCls:
	"""Up commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("up", core, parent)

	def set(self, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex<CH0>:UP \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.segment.index.up.set(indexNull = repcap.IndexNull.Default) \n
		Shifts the selected waveform segment up by one segment in the segment table. \n
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Index')
		"""
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex{indexNull_cmd_val}:UP')

	def set_with_opc(self, indexNull=repcap.IndexNull.Default, opc_timeout_ms: int = -1) -> None:
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex<CH0>:UP \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.segment.index.up.set_with_opc(indexNull = repcap.IndexNull.Default) \n
		Shifts the selected waveform segment up by one segment in the segment table. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Index')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex{indexNull_cmd_val}:UP', opc_timeout_ms)
