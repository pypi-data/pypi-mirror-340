from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HdbCls:
	"""Hdb commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hdb", core, parent)

	@property
	def sic(self):
		"""sic commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sic'):
			from .Sic import SicCls
			self._sic = SicCls(self._core, self._cmd_group)
		return self._sic

	def get_dmcs(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:DMCS \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hdb.get_dmcs() \n
		Sets the differential EDMG modulation and coding scheme (MCS) . The corresponding field is a 2-bit field after the Base
		MCS field of the EDMG-Header-B field. \n
			:return: diff_mcs: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:DMCS?')
		return Conversions.str_to_int(response)

	def set_dmcs(self, diff_mcs: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:DMCS \n
		Snippet: driver.source.bb.wlay.pconfig.hdb.set_dmcs(diff_mcs = 1) \n
		Sets the differential EDMG modulation and coding scheme (MCS) . The corresponding field is a 2-bit field after the Base
		MCS field of the EDMG-Header-B field. \n
			:param diff_mcs: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(diff_mcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:DMCS {param}')

	def get_scrs(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:SCRS \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hdb.get_scrs() \n
		Sets the scrambler seed value. The corresponding field is a 7-bit field at the beginning of the EDMG-Header-B field. \n
			:return: scra_seed: integer Range: 0 to 63
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:SCRS?')
		return Conversions.str_to_int(response)

	def set_scrs(self, scra_seed: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDB:SCRS \n
		Snippet: driver.source.bb.wlay.pconfig.hdb.set_scrs(scra_seed = 1) \n
		Sets the scrambler seed value. The corresponding field is a 7-bit field at the beginning of the EDMG-Header-B field. \n
			:param scra_seed: integer Range: 0 to 63
		"""
		param = Conversions.decimal_value_to_str(scra_seed)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDB:SCRS {param}')

	def clone(self) -> 'HdbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HdbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
