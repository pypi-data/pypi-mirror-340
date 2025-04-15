from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SscCls:
	"""Ssc commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ssc", core, parent)

	@property
	def sfi(self):
		"""sfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfi'):
			from .Sfi import SfiCls
			self._sfi = SfiCls(self._core, self._cmd_group)
		return self._sfi

	def get_ndl_symbols(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NDLSymbols \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.ssc.get_ndl_symbols() \n
		Defines the number of downlink symbols in a special slot.
			INTRO_CMD_HELP: Prerequisites to define the number of downlink symbols: \n
			- Enter downlink mode ([:SOURce<hw>]:BB:NR5G:LINK) .
			- Turn off usage of special slot format ([:SOURce<hw>]:BB:NR5G:QCKSet:FRMFormat:SSC:SFI:STATe) .
		Otherwise, the command is a query only. \n
			:return: qck_set_slot_dl_sym: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NDLSymbols?')
		return Conversions.str_to_int(response)

	def get_ng_symbols(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NGSYmbols \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.ssc.get_ng_symbols() \n
		Queries the number of guard symbols. \n
			:return: qck_set_sguard_sym: integer Range: 0 to 14
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NGSYmbols?')
		return Conversions.str_to_int(response)

	def get_nul_symbols(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NULSymbols \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.ssc.get_nul_symbols() \n
		Defines the number of uplink symbols in a special slot.
			INTRO_CMD_HELP: Prerequisites to define the number of downlink symbols: \n
			- Enter uplink mode ([:SOURce<hw>]:BB:NR5G:LINK) .
			- Turn off usage of special slot format ([:SOURce<hw>]:BB:NR5G:QCKSet:FRMFormat:SSC:SFI:STATe) .
		Otherwise, the command is a query only. \n
			:return: qck_set_sul_slots: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NULSymbols?')
		return Conversions.str_to_int(response)

	def get_slfmt(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.ssc.get_slfmt() \n
		Sets the special slot format index. \n
			:return: qck_set_slot_fmt: integer Range: 0 to 45
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'SscCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SscCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
