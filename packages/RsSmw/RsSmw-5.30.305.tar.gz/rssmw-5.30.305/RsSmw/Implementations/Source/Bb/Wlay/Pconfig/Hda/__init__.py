from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HdaCls:
	"""Hda commands group definition. 17 total commands, 7 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hda", core, parent)

	@property
	def aggregate(self):
		"""aggregate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aggregate'):
			from .Aggregate import AggregateCls
			self._aggregate = AggregateCls(self._core, self._cmd_group)
		return self._aggregate

	@property
	def bf(self):
		"""bf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bf'):
			from .Bf import BfCls
			self._bf = BfCls(self._core, self._cmd_group)
		return self._bf

	@property
	def lldpc(self):
		"""lldpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lldpc'):
			from .Lldpc import LldpcCls
			self._lldpc = LldpcCls(self._core, self._cmd_group)
		return self._lldpc

	@property
	def mcs(self):
		"""mcs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def mu(self):
		"""mu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mu'):
			from .Mu import MuCls
			self._mu = MuCls(self._core, self._cmd_group)
		return self._mu

	@property
	def nuc(self):
		"""nuc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nuc'):
			from .Nuc import NucCls
			self._nuc = NucCls(self._core, self._cmd_group)
		return self._nuc

	@property
	def stbc(self):
		"""stbc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbc'):
			from .Stbc import StbcCls
			self._stbc = StbcCls(self._core, self._cmd_group)
		return self._stbc

	def get_bmcs(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BMCS \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_bmcs() \n
		Selects the modulation and coding scheme (MCS) for all spatial streams. The current firmware supports MSC for EDMG SC
		mode only, see Table 'MCS for IEEE 802.11ay EDMG SC mode', for example. \n
			:return: base_mcs: integer Range: 1 to 21
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BMCS?')
		return Conversions.str_to_int(response)

	def set_bmcs(self, base_mcs: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BMCS \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_bmcs(base_mcs = 1) \n
		Selects the modulation and coding scheme (MCS) for all spatial streams. The current firmware supports MSC for EDMG SC
		mode only, see Table 'MCS for IEEE 802.11ay EDMG SC mode', for example. \n
			:param base_mcs: integer Range: 1 to 21
		"""
		param = Conversions.decimal_value_to_str(base_mcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BMCS {param}')

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.WlanayBw:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BW \n
		Snippet: value: enums.WlanayBw = driver.source.bb.wlay.pconfig.hda.get_bw() \n
		Sets the bandwidth of the EDMG single carrier signal that is a multiple of 2.16 GHz. \n
			:return: bw: BW216| BW432 BW216 2.16 GHz bandwidth BW432 Requires R&S SMW-K555. 4.32 GHz bandwidth
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BW?')
		return Conversions.str_to_scalar_enum(response, enums.WlanayBw)

	def set_bw(self, bw: enums.WlanayBw) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:BW \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_bw(bw = enums.WlanayBw.BW216) \n
		Sets the bandwidth of the EDMG single carrier signal that is a multiple of 2.16 GHz. \n
			:param bw: BW216| BW432 BW216 2.16 GHz bandwidth BW432 Requires R&S SMW-K555. 4.32 GHz bandwidth
		"""
		param = Conversions.enum_scalar_to_str(bw, enums.WlanayBw)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:BW {param}')

	def get_cconfig(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:CCONfig \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_cconfig() \n
		Sets the channel configuration that is the configuration 2.16 GHz and 4.32 GHz channels. \n
			:return: channel_config: integer Range: 1 to 176
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:CCONfig?')
		return Conversions.str_to_int(response)

	def set_cconfig(self, channel_config: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:CCONfig \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_cconfig(channel_config = 1) \n
		Sets the channel configuration that is the configuration 2.16 GHz and 4.32 GHz channels. \n
			:param channel_config: integer Range: 1 to 176
		"""
		param = Conversions.decimal_value_to_str(channel_config)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:CCONfig {param}')

	def get_pchannel(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:PCHannel \n
		Snippet: value: float = driver.source.bb.wlay.pconfig.hda.get_pchannel() \n
		Queries the primary channel number as set via the channel configuration, see Table 'Channels of an EDMG STA'. \n
			:return: primary_cha: float Range: 1 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:PCHannel?')
		return Conversions.str_to_float(response)

	def get_rtpt(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:RTPT \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_rtpt() \n
		Sets the number of receive (RX) TRN units per transmit (TX) TRN unit. \n
			:return: rx_trn_tx_trn: integer Range: 1 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:RTPT?')
		return Conversions.str_to_int(response)

	def set_rtpt(self, rx_trn_tx_trn: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:RTPT \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_rtpt(rx_trn_tx_trn = 1) \n
		Sets the number of receive (RX) TRN units per transmit (TX) TRN unit. \n
			:param rx_trn_tx_trn: integer Range: 1 to 255
		"""
		param = Conversions.decimal_value_to_str(rx_trn_tx_trn)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:RTPT {param}')

	def get_trn_m(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNM \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_trn_m() \n
		Sets the bits in the 4-bit EDMG TRN-Unit M field. \n
			:return: trn_m: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNM?')
		return Conversions.str_to_int(response)

	def set_trn_m(self, trn_m: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNM \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_trn_m(trn_m = 1) \n
		Sets the bits in the 4-bit EDMG TRN-Unit M field. \n
			:param trn_m: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(trn_m)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNM {param}')

	def get_trn_n(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNN \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_trn_n() \n
		Sets the bits in the 2-bit EDMG TRN-Unit N field. \n
			:return: trn_n: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNN?')
		return Conversions.str_to_int(response)

	def set_trn_n(self, trn_n: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNN \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_trn_n(trn_n = 1) \n
		Sets the bits in the 2-bit EDMG TRN-Unit N field. \n
			:param trn_n: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(trn_n)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNN {param}')

	def get_trn_p(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNP \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.hda.get_trn_p() \n
		Sets the bits in the 2-bit EDMG TRN-Unit P field. \n
			:return: trn_p: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNP?')
		return Conversions.str_to_int(response)

	def set_trn_p(self, trn_p: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TRNP \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_trn_p(trn_p = 1) \n
		Sets the bits in the 2-bit EDMG TRN-Unit P field. \n
			:param trn_p: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(trn_p)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TRNP {param}')

	# noinspection PyTypeChecker
	def get_tsl(self) -> enums.SequenceLength:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TSL \n
		Snippet: value: enums.SequenceLength = driver.source.bb.wlay.pconfig.hda.get_tsl() \n
		Sets training sequence length as set with the 2-bit subfield 'Sequence Length' of the TRN field. \n
			:return: trn_seq_len: NORMAL| LONG| SHORT NORMAL Normal sequence length of 128 x NCB with subfield value 0. LONG Long sequence length of 256 x NCB with subfield value 1. SHORT Short sequence length of 64 x NCB with subfield value 2.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TSL?')
		return Conversions.str_to_scalar_enum(response, enums.SequenceLength)

	def set_tsl(self, trn_seq_len: enums.SequenceLength) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:HDA:TSL \n
		Snippet: driver.source.bb.wlay.pconfig.hda.set_tsl(trn_seq_len = enums.SequenceLength.LONG) \n
		Sets training sequence length as set with the 2-bit subfield 'Sequence Length' of the TRN field. \n
			:param trn_seq_len: NORMAL| LONG| SHORT NORMAL Normal sequence length of 128 x NCB with subfield value 0. LONG Long sequence length of 256 x NCB with subfield value 1. SHORT Short sequence length of 64 x NCB with subfield value 2.
		"""
		param = Conversions.enum_scalar_to_str(trn_seq_len, enums.SequenceLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:HDA:TSL {param}')

	def clone(self) -> 'HdaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HdaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
