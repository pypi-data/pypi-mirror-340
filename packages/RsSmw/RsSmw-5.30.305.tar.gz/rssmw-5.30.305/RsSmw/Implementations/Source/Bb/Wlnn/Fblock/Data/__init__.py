from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 6 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def dcycle(self):
		"""dcycle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcycle'):
			from .Dcycle import DcycleCls
			self._dcycle = DcycleCls(self._core, self._cmd_group)
		return self._dcycle

	@property
	def dselection(self):
		"""dselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselection'):
			from .Dselection import DselectionCls
			self._dselection = DselectionCls(self._core, self._cmd_group)
		return self._dselection

	@property
	def fdelay(self):
		"""fdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdelay'):
			from .Fdelay import FdelayCls
			self._fdelay = FdelayCls(self._core, self._cmd_group)
		return self._fdelay

	@property
	def fduration(self):
		"""fduration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fduration'):
			from .Fduration import FdurationCls
			self._fduration = FdurationCls(self._core, self._cmd_group)
		return self._fduration

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	def set(self, data: enums.WlannDataSource, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA \n
		Snippet: driver.source.bb.wlnn.fblock.data.set(data = enums.WlannDataSource.AMPDU, frameBlock = repcap.FrameBlock.Default) \n
		Selects the data source. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLocks:DATA:DSEL ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLocks:DATA:PATTern. AMPDU Aggregated mac protocol data unit (A-MPDU) data is used as configured with the commands in 'MPDU configuration'
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.enum_scalar_to_str(data, enums.WlannDataSource)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default) -> enums.WlannDataSource:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA \n
		Snippet: value: enums.WlannDataSource = driver.source.bb.wlnn.fblock.data.get(frameBlock = repcap.FrameBlock.Default) \n
		Selects the data source. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLocks:DATA:DSEL ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLocks:DATA:PATTern. AMPDU Aggregated mac protocol data unit (A-MPDU) data is used as configured with the commands in 'MPDU configuration'"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.WlannDataSource)

	def clone(self) -> 'DataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
