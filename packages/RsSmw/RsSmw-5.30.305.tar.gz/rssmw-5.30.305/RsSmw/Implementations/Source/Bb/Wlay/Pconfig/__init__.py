from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PconfigCls:
	"""Pconfig commands group definition. 32 total commands, 5 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pconfig", core, parent)

	@property
	def hda(self):
		"""hda commands group. 7 Sub-classes, 9 commands."""
		if not hasattr(self, '_hda'):
			from .Hda import HdaCls
			self._hda = HdaCls(self._core, self._cmd_group)
		return self._hda

	@property
	def hdb(self):
		"""hdb commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_hdb'):
			from .Hdb import HdbCls
			self._hdb = HdbCls(self._core, self._cmd_group)
		return self._hdb

	@property
	def lhdr(self):
		"""lhdr commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_lhdr'):
			from .Lhdr import LhdrCls
			self._lhdr = LhdrCls(self._core, self._cmd_group)
		return self._lhdr

	@property
	def psk(self):
		"""psk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psk'):
			from .Psk import PskCls
			self._psk = PskCls(self._core, self._cmd_group)
		return self._psk

	@property
	def uconfig(self):
		"""uconfig commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_uconfig'):
			from .Uconfig import UconfigCls
			self._uconfig = UconfigCls(self._core, self._cmd_group)
		return self._uconfig

	def get_bsb_number(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:BSBNumber \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.get_bsb_number() \n
		Sets the minimum duration of data. \n
			:return: brp_min_sc_blk_num: integer Range: 1 to 18
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:BSBNumber?')
		return Conversions.str_to_int(response)

	def set_bsb_number(self, brp_min_sc_blk_num: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:BSBNumber \n
		Snippet: driver.source.bb.wlay.pconfig.set_bsb_number(brp_min_sc_blk_num = 1) \n
		Sets the minimum duration of data. \n
			:param brp_min_sc_blk_num: integer Range: 1 to 18
		"""
		param = Conversions.decimal_value_to_str(brp_min_sc_blk_num)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:BSBNumber {param}')

	def get_csd_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:CSDState \n
		Snippet: value: bool = driver.source.bb.wlay.pconfig.get_csd_state() \n
		Activates cyclic shift diversity (CSD) . \n
			:return: csd_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:CSDState?')
		return Conversions.str_to_bool(response)

	def set_csd_state(self, csd_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:CSDState \n
		Snippet: driver.source.bb.wlay.pconfig.set_csd_state(csd_state = False) \n
		Activates cyclic shift diversity (CSD) . \n
			:param csd_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(csd_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:CSDState {param}')

	def get_ss_number(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:SSNumber \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.get_ss_number() \n
		Queries the number of spatial streams. \n
			:return: ss_num: integer Range: 1 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:SSNumber?')
		return Conversions.str_to_int(response)

	def set_ss_number(self, ss_num: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:SSNumber \n
		Snippet: driver.source.bb.wlay.pconfig.set_ss_number(ss_num = 1) \n
		Queries the number of spatial streams. \n
			:param ss_num: integer Range: 1 to 8
		"""
		param = Conversions.decimal_value_to_str(ss_num)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:SSNumber {param}')

	# noinspection PyTypeChecker
	def get_traggregate(self) -> enums.WlanadTrnAggregate:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:TRAGgregate \n
		Snippet: value: enums.WlanadTrnAggregate = driver.source.bb.wlay.pconfig.get_traggregate() \n
		Sets the training (TRN) aggregation mode. The modes are defined by the 1-bit TRN Aggregation field of the EDMG-Header-A2
		subfield. \n
			:return: trn_aggregate: WB| ATRN WB WidebandTRN TRN Aggregation field is 0. The bandwidth (BW) field specifies that the TRN field of the PPDU is appended on a 2.16 GHz, 4.32 GHz, 6.48 GHz, or 8.64 GHz channel. ATRN AggregationTRN TRN Aggregation field is 1. The BW field specifies that the TRN field is transmitted over a 2.16+2.16 GHz or 4.32+4.32 GHz channel.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:TRAGgregate?')
		return Conversions.str_to_scalar_enum(response, enums.WlanadTrnAggregate)

	def set_traggregate(self, trn_aggregate: enums.WlanadTrnAggregate) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:TRAGgregate \n
		Snippet: driver.source.bb.wlay.pconfig.set_traggregate(trn_aggregate = enums.WlanadTrnAggregate.ATRN) \n
		Sets the training (TRN) aggregation mode. The modes are defined by the 1-bit TRN Aggregation field of the EDMG-Header-A2
		subfield. \n
			:param trn_aggregate: WB| ATRN WB WidebandTRN TRN Aggregation field is 0. The bandwidth (BW) field specifies that the TRN field of the PPDU is appended on a 2.16 GHz, 4.32 GHz, 6.48 GHz, or 8.64 GHz channel. ATRN AggregationTRN TRN Aggregation field is 1. The BW field specifies that the TRN field is transmitted over a 2.16+2.16 GHz or 4.32+4.32 GHz channel.
		"""
		param = Conversions.enum_scalar_to_str(trn_aggregate, enums.WlanadTrnAggregate)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:TRAGgregate {param}')

	def get_usr_number(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:USRNumber \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.get_usr_number() \n
		Queries the number of users. The maximum number of users equals the maximum number of spatial streams that is 8. \n
			:return: usr_num: integer Range: 1 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:USRNumber?')
		return Conversions.str_to_int(response)

	def set_usr_number(self, usr_num: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:USRNumber \n
		Snippet: driver.source.bb.wlay.pconfig.set_usr_number(usr_num = 1) \n
		Queries the number of users. The maximum number of users equals the maximum number of spatial streams that is 8. \n
			:param usr_num: integer Range: 1 to 8
		"""
		param = Conversions.decimal_value_to_str(usr_num)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:USRNumber {param}')

	def clone(self) -> 'PconfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PconfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
