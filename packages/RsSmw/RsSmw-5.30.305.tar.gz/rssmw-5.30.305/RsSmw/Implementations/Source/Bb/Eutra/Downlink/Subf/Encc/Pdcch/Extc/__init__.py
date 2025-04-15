from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtcCls:
	"""Extc commands group definition. 67 total commands, 9 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extc", core, parent)

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Append import AppendCls
			self._append = AppendCls(self._core, self._cmd_group)
		return self._append

	@property
	def conflicts(self):
		"""conflicts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflicts'):
			from .Conflicts import ConflictsCls
			self._conflicts = ConflictsCls(self._core, self._cmd_group)
		return self._conflicts

	@property
	def down(self):
		"""down commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_down'):
			from .Down import DownCls
			self._down = DownCls(self._core, self._cmd_group)
		return self._down

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Insert import InsertCls
			self._insert = InsertCls(self._core, self._cmd_group)
		return self._insert

	@property
	def item(self):
		"""item commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_item'):
			from .Item import ItemCls
			self._item = ItemCls(self._core, self._cmd_group)
		return self._item

	@property
	def sitem(self):
		"""sitem commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sitem'):
			from .Sitem import SitemCls
			self._sitem = SitemCls(self._core, self._cmd_group)
		return self._sitem

	@property
	def solve(self):
		"""solve commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_solve'):
			from .Solve import SolveCls
			self._solve = SolveCls(self._core, self._cmd_group)
		return self._solve

	@property
	def uitems(self):
		"""uitems commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uitems'):
			from .Uitems import UitemsCls
			self._uitems = UitemsCls(self._core, self._cmd_group)
		return self._uitems

	@property
	def up(self):
		"""up commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_up'):
			from .Up import UpCls
			self._up = UpCls(self._core, self._cmd_group)
		return self._up

	def delete(self, subframeNull=repcap.SubframeNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:DELete \n
		Snippet: driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.delete(subframeNull = repcap.SubframeNull.Default) \n
		Deletes the selected row. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
		"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:DELete')

	def delete_with_opc(self, subframeNull=repcap.SubframeNull.Default, opc_timeout_ms: int = -1) -> None:
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:DELete \n
		Snippet: driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.delete_with_opc(subframeNull = repcap.SubframeNull.Default) \n
		Deletes the selected row. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:DELete', opc_timeout_ms)

	def reset(self, subframeNull=repcap.SubframeNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:RESet \n
		Snippet: driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.reset(subframeNull = repcap.SubframeNull.Default) \n
		Resets the table. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
		"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:RESet')

	def reset_with_opc(self, subframeNull=repcap.SubframeNull.Default, opc_timeout_ms: int = -1) -> None:
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST0>]:ENCC:PDCCh:EXTC:RESet \n
		Snippet: driver.source.bb.eutra.downlink.subf.encc.pdcch.extc.reset_with_opc(subframeNull = repcap.SubframeNull.Default) \n
		Resets the table. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{subframeNull_cmd_val}:ENCC:PDCCh:EXTC:RESet', opc_timeout_ms)

	def clone(self) -> 'ExtcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExtcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
