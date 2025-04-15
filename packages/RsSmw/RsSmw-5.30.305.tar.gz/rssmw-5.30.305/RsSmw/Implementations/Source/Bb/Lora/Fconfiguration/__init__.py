from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FconfigurationCls:
	"""Fconfiguration commands group definition. 16 total commands, 9 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fconfiguration", core, parent)

	@property
	def bmode(self):
		"""bmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmode'):
			from .Bmode import BmodeCls
			self._bmode = BmodeCls(self._core, self._cmd_group)
		return self._bmode

	@property
	def cmode(self):
		"""cmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmode'):
			from .Cmode import CmodeCls
			self._cmode = CmodeCls(self._core, self._cmd_group)
		return self._cmode

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def eactive(self):
		"""eactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eactive'):
			from .Eactive import EactiveCls
			self._eactive = EactiveCls(self._core, self._cmd_group)
		return self._eactive

	@property
	def hactive(self):
		"""hactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hactive'):
			from .Hactive import HactiveCls
			self._hactive = HactiveCls(self._core, self._cmd_group)
		return self._hactive

	@property
	def iactive(self):
		"""iactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iactive'):
			from .Iactive import IactiveCls
			self._iactive = IactiveCls(self._core, self._cmd_group)
		return self._iactive

	@property
	def pcRc(self):
		"""pcRc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcRc'):
			from .PcRc import PcRcCls
			self._pcRc = PcRcCls(self._core, self._cmd_group)
		return self._pcRc

	@property
	def prcMode(self):
		"""prcMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prcMode'):
			from .PrcMode import PrcModeCls
			self._prcMode = PrcModeCls(self._core, self._cmd_group)
		return self._prcMode

	@property
	def rbit(self):
		"""rbit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbit'):
			from .Rbit import RbitCls
			self._rbit = RbitCls(self._core, self._cmd_group)
		return self._rbit

	# noinspection PyTypeChecker
	def get_crate(self) -> enums.LoRaCodRate:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:CRATe \n
		Snippet: value: enums.LoRaCodRate = driver.source.bb.lora.fconfiguration.get_crate() \n
		Sets the coding rate. \n
			:return: crate: CR0| CR1| CR2| CR3| CR4 CRx = 0 to 4 The coding rate RCoding is calculated as follows: RCoding = 4 / (4 + CRx) 'CR0' corresponds to no coding, i.e. RCoding = 1.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:CRATe?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaCodRate)

	def set_crate(self, crate: enums.LoRaCodRate) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:CRATe \n
		Snippet: driver.source.bb.lora.fconfiguration.set_crate(crate = enums.LoRaCodRate.CR0) \n
		Sets the coding rate. \n
			:param crate: CR0| CR1| CR2| CR3| CR4 CRx = 0 to 4 The coding rate RCoding is calculated as follows: RCoding = 4 / (4 + CRx) 'CR0' corresponds to no coding, i.e. RCoding = 1.
		"""
		param = Conversions.enum_scalar_to_str(crate, enums.LoRaCodRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:CRATe {param}')

	def get_dlength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:DLENgth \n
		Snippet: value: int = driver.source.bb.lora.fconfiguration.get_dlength() \n
		Sets the data length of the payload in the frame. \n
			:return: dlength: integer Range: 1 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:DLENgth?')
		return Conversions.str_to_int(response)

	def set_dlength(self, dlength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:DLENgth \n
		Snippet: driver.source.bb.lora.fconfiguration.set_dlength(dlength = 1) \n
		Sets the data length of the payload in the frame. \n
			:param dlength: integer Range: 1 to 255
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:DLENgth {param}')

	# noinspection PyTypeChecker
	def get_sfactor(self) -> enums.LoRaSf:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:SFACtor \n
		Snippet: value: enums.LoRaSf = driver.source.bb.lora.fconfiguration.get_sfactor() \n
		Sets the spreading factor for the modulation. \n
			:return: sf: SF6| SF7| SF8| SF9| SF10| SF11| SF12
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:SFACtor?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaSf)

	def set_sfactor(self, sf: enums.LoRaSf) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:SFACtor \n
		Snippet: driver.source.bb.lora.fconfiguration.set_sfactor(sf = enums.LoRaSf.SF10) \n
		Sets the spreading factor for the modulation. \n
			:param sf: SF6| SF7| SF8| SF9| SF10| SF11| SF12
		"""
		param = Conversions.enum_scalar_to_str(sf, enums.LoRaSf)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:SFACtor {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.LoRaSyncMode:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:SMODe \n
		Snippet: value: enums.LoRaSyncMode = driver.source.bb.lora.fconfiguration.get_smode() \n
		Sets the synchronization mode of the preamble. \n
			:return: smode: PRIVate| PUBLic PRIVate A preamble with a public sync word is generated. PUBLic A preamble with a private sync word is generated.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaSyncMode)

	def set_smode(self, smode: enums.LoRaSyncMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:SMODe \n
		Snippet: driver.source.bb.lora.fconfiguration.set_smode(smode = enums.LoRaSyncMode.PRIVate) \n
		Sets the synchronization mode of the preamble. \n
			:param smode: PRIVate| PUBLic PRIVate A preamble with a public sync word is generated. PUBLic A preamble with a private sync word is generated.
		"""
		param = Conversions.enum_scalar_to_str(smode, enums.LoRaSyncMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:SMODe {param}')

	def get_up_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:UPLength \n
		Snippet: value: int = driver.source.bb.lora.fconfiguration.get_up_length() \n
		Sets the unmodulated preamble length. \n
			:return: plength: integer Range: 6 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:UPLength?')
		return Conversions.str_to_int(response)

	def set_up_length(self, plength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:LORA:FCONfiguration:UPLength \n
		Snippet: driver.source.bb.lora.fconfiguration.set_up_length(plength = 1) \n
		Sets the unmodulated preamble length. \n
			:param plength: integer Range: 6 to 8
		"""
		param = Conversions.decimal_value_to_str(plength)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:UPLength {param}')

	def clone(self) -> 'FconfigurationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FconfigurationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
