from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IndexCls:
	"""Index commands group definition. 3 total commands, 2 Subgroups, 1 group commands
	Repeated Capability: IndexNull, default value after init: IndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("index", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_indexNull_get', 'repcap_indexNull_set', repcap.IndexNull.Nr0)

	def repcap_indexNull_set(self, indexNull: repcap.IndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndexNull.Default.
		Default value after init: IndexNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(indexNull)

	def repcap_indexNull_get(self) -> repcap.IndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def down(self):
		"""down commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_down'):
			from .Down import DownCls
			self._down = DownCls(self._core, self._cmd_group)
		return self._down

	@property
	def up(self):
		"""up commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_up'):
			from .Up import UpCls
			self._up = UpCls(self._core, self._cmd_group)
		return self._up

	def delete(self, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex<CH0>:DELete \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.segment.index.delete(indexNull = repcap.IndexNull.Default) \n
		Deletes the selected waveform segment in the segment table. \n
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Index')
		"""
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex{indexNull_cmd_val}:DELete')

	def delete_with_opc(self, indexNull=repcap.IndexNull.Default, opc_timeout_ms: int = -1) -> None:
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex<CH0>:DELete \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.segment.index.delete_with_opc(indexNull = repcap.IndexNull.Default) \n
		Deletes the selected waveform segment in the segment table. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Index')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:INDex{indexNull_cmd_val}:DELete', opc_timeout_ms)

	def clone(self) -> 'IndexCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IndexCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
