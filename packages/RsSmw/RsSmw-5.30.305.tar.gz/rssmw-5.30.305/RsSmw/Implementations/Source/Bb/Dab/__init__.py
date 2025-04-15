from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DabCls:
	"""Dab commands group definition. 54 total commands, 11 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dab", core, parent)

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def coder(self):
		"""coder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coder'):
			from .Coder import CoderCls
			self._coder = CoderCls(self._core, self._cmd_group)
		return self._coder

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def eti(self):
		"""eti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eti'):
			from .Eti import EtiCls
			self._eti = EtiCls(self._core, self._cmd_group)
		return self._eti

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def ileaver(self):
		"""ileaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ileaver'):
			from .Ileaver import IleaverCls
			self._ileaver = IleaverCls(self._core, self._cmd_group)
		return self._ileaver

	@property
	def pnScrambler(self):
		"""pnScrambler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnScrambler'):
			from .PnScrambler import PnScramblerCls
			self._pnScrambler = PnScramblerCls(self._core, self._cmd_group)
		return self._pnScrambler

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def tii(self):
		"""tii commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tii'):
			from .Tii import TiiCls
			self._tii = TiiCls(self._core, self._cmd_group)
		return self._tii

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	def get_eframes(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:DAB:EFRames \n
		Snippet: value: float = driver.source.bb.dab.get_eframes() \n
		No command help available \n
			:return: eframes: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:EFRames?')
		return Conversions.str_to_float(response)

	def set_eframes(self, eframes: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:EFRames \n
		Snippet: driver.source.bb.dab.set_eframes(eframes = 1.0) \n
		No command help available \n
			:param eframes: No help available
		"""
		param = Conversions.decimal_value_to_str(eframes)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:EFRames {param}')

	def get_lduration(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:DAB:LDURation \n
		Snippet: value: float = driver.source.bb.dab.get_lduration() \n
		No command help available \n
			:return: lduration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:LDURation?')
		return Conversions.str_to_float(response)

	def get_mid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DAB:MID \n
		Snippet: value: int = driver.source.bb.dab.get_mid() \n
		No command help available \n
			:return: mid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:MID?')
		return Conversions.str_to_int(response)

	def set_mid(self, mid: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:MID \n
		Snippet: driver.source.bb.dab.set_mid(mid = 1) \n
		No command help available \n
			:param mid: No help available
		"""
		param = Conversions.decimal_value_to_str(mid)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:MID {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:PRESet \n
		Snippet: driver.source.bb.dab.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:PRESet \n
		Snippet: driver.source.bb.dab.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DAB:PRESet', opc_timeout_ms)

	def get_sid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DAB:SID \n
		Snippet: value: int = driver.source.bb.dab.get_sid() \n
		No command help available \n
			:return: sid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:SID?')
		return Conversions.str_to_int(response)

	def set_sid(self, sid: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:SID \n
		Snippet: driver.source.bb.dab.set_sid(sid = 1) \n
		No command help available \n
			:param sid: No help available
		"""
		param = Conversions.decimal_value_to_str(sid)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:SID {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DAB:STATe \n
		Snippet: value: bool = driver.source.bb.dab.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:STATe \n
		Snippet: driver.source.bb.dab.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:STATe {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.DabTxMode:
		"""SCPI: [SOURce<HW>]:BB:DAB:TMODe \n
		Snippet: value: enums.DabTxMode = driver.source.bb.dab.get_tmode() \n
		No command help available \n
			:return: tmode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.DabTxMode)

	def set_tmode(self, tmode: enums.DabTxMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:TMODe \n
		Snippet: driver.source.bb.dab.set_tmode(tmode = enums.DabTxMode.I) \n
		No command help available \n
			:param tmode: No help available
		"""
		param = Conversions.enum_scalar_to_str(tmode, enums.DabTxMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:TMODe {param}')

	def clone(self) -> 'DabCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DabCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
