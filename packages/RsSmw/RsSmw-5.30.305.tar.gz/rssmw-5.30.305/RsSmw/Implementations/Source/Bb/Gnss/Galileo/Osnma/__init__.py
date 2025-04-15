from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OsnmaCls:
	"""Osnma commands group definition. 20 total commands, 4 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osnma", core, parent)

	@property
	def aesKey(self):
		"""aesKey commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aesKey'):
			from .AesKey import AesKeyCls
			self._aesKey = AesKeyCls(self._core, self._cmd_group)
		return self._aesKey

	@property
	def ckey(self):
		"""ckey commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ckey'):
			from .Ckey import CkeyCls
			self._ckey = CkeyCls(self._core, self._cmd_group)
		return self._ckey

	@property
	def pkey(self):
		"""pkey commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pkey'):
			from .Pkey import PkeyCls
			self._pkey = PkeyCls(self._core, self._cmd_group)
		return self._pkey

	@property
	def rkey(self):
		"""rkey commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rkey'):
			from .Rkey import RkeyCls
			self._rkey = RkeyCls(self._core, self._cmd_group)
		return self._rkey

	def get_ad_delay(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADDelay \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_ad_delay() \n
		Sets an additional delay in subframes of the navigation data for the tag verification. The delay can depend on receiver
		implementation. You can set a delay of one subframe. A zero subframe delay corresponds to no delay. \n
			:return: delay: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADDelay?')
		return Conversions.str_to_int(response)

	def set_ad_delay(self, delay: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADDelay \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ad_delay(delay = 1) \n
		Sets an additional delay in subframes of the navigation data for the tag verification. The delay can depend on receiver
		implementation. You can set a delay of one subframe. A zero subframe delay corresponds to no delay. \n
			:param delay: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADDelay {param}')

	def get_adkd(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADKD \n
		Snippet: value: bool = driver.source.bb.gnss.galileo.osnma.get_adkd() \n
		Enable the authentication data and key delay (ADKD) for ADKD=4 for Galileo I/NAV timing parameters. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADKD?')
		return Conversions.str_to_bool(response)

	def set_adkd(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADKD \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_adkd(state = False) \n
		Enable the authentication data and key delay (ADKD) for ADKD=4 for Galileo I/NAV timing parameters. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADKD {param}')

	# noinspection PyTypeChecker
	def get_hf(self) -> enums.OsnmaHf:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:HF \n
		Snippet: value: enums.OsnmaHf = driver.source.bb.gnss.galileo.osnma.get_hf() \n
		Sets the bits in the 2-bit Hash Function (HF) field. \n
			:return: value: 0| 2 For a description on HF values, see Table 'HF value and hash function'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:HF?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaHf)

	def set_hf(self, value: enums.OsnmaHf) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:HF \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_hf(value = enums.OsnmaHf._0) \n
		Sets the bits in the 2-bit Hash Function (HF) field. \n
			:param value: 0| 2 For a description on HF values, see Table 'HF value and hash function'.
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaHf)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:HF {param}')

	# noinspection PyTypeChecker
	def get_ks(self) -> enums.OsnmaKs:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:KS \n
		Snippet: value: enums.OsnmaKs = driver.source.bb.gnss.galileo.osnma.get_ks() \n
		Sets the bits in the 4-bit Key Size (KS) field. \n
			:return: value: 0| 1| 2| 3| 4| 5| 6| 7| 8 For a description on KS values, see Table 'KS value and key length'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:KS?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaKs)

	def set_ks(self, value: enums.OsnmaKs) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:KS \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ks(value = enums.OsnmaKs._0) \n
		Sets the bits in the 4-bit Key Size (KS) field. \n
			:param value: 0| 1| 2| 3| 4| 5| 6| 7| 8 For a description on KS values, see Table 'KS value and key length'.
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaKs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:KS {param}')

	# noinspection PyTypeChecker
	def get_mac_lt(self) -> enums.OsnmaMaclt:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MACLt \n
		Snippet: value: enums.OsnmaMaclt = driver.source.bb.gnss.galileo.osnma.get_mac_lt() \n
		Sets the bits in the 8-bit MAC Look-up Table (MACLT) field. \n
			:return: value: 27| 28| 31| 33| 34| 35| 36| 37| 38| 39| 40| 41
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MACLt?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaMaclt)

	def set_mac_lt(self, value: enums.OsnmaMaclt) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MACLt \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_mac_lt(value = enums.OsnmaMaclt._27) \n
		Sets the bits in the 8-bit MAC Look-up Table (MACLT) field. \n
			:param value: 27| 28| 31| 33| 34| 35| 36| 37| 38| 39| 40| 41
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaMaclt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MACLt {param}')

	def get_mf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MF \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_mf() \n
		Sets the bits in the 2-bit MAC Function (MF) field. \n
			:return: mf: integer For a description on MF values, see Table 'MF value and hash function'. Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MF?')
		return Conversions.str_to_int(response)

	def set_mf(self, mf: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MF \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_mf(mf = 1) \n
		Sets the bits in the 2-bit MAC Function (MF) field. \n
			:param mf: integer For a description on MF values, see Table 'MF value and hash function'. Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(mf)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MF {param}')

	# noinspection PyTypeChecker
	def get_npkt(self) -> enums.OsnmaNpkt:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:NPKT \n
		Snippet: value: enums.OsnmaNpkt = driver.source.bb.gnss.galileo.osnma.get_npkt() \n
		Sets the bits in the 4-bit New Public Key Type (NPKT) field. This field represents the signature algorithm associated
		with the public key provided in the digital signature message for a public key renewal (DSM-PKR) . \n
			:return: value: 1| 3 For a description on NPKT values, see Table 'NPKT value and message type'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:NPKT?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaNpkt)

	def set_npkt(self, value: enums.OsnmaNpkt) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:NPKT \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_npkt(value = enums.OsnmaNpkt._1) \n
		Sets the bits in the 4-bit New Public Key Type (NPKT) field. This field represents the signature algorithm associated
		with the public key provided in the digital signature message for a public key renewal (DSM-PKR) . \n
			:param value: 1| 3 For a description on NPKT values, see Table 'NPKT value and message type'.
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaNpkt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:NPKT {param}')

	def get_pid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PID \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_pid() \n
		Sets the ID of the Public Key (PK) used to verify the signature of the digital signature message for a root key
		(DSM-KROOT) . If the transition mode defines the change of the public key, the PKID depends on the simulation time. This
		PKID means the public key which is currently in use and the PKID is increased by each public key transition. \n
			:return: pid_input_2: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PID?')
		return Conversions.str_to_int(response)

	def set_pid(self, pid_input_2: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PID \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_pid(pid_input_2 = 1) \n
		Sets the ID of the Public Key (PK) used to verify the signature of the digital signature message for a root key
		(DSM-KROOT) . If the transition mode defines the change of the public key, the PKID depends on the simulation time. This
		PKID means the public key which is currently in use and the PKID is increased by each public key transition. \n
			:param pid_input_2: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(pid_input_2)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PID {param}')

	def get_spreemption(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:SPReemption \n
		Snippet: value: bool = driver.source.bb.gnss.galileo.osnma.get_spreemption() \n
		Enable the status preemption. \n
			:return: status: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:SPReemption?')
		return Conversions.str_to_bool(response)

	def set_spreemption(self, status: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:SPReemption \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_spreemption(status = False) \n
		Enable the status preemption. \n
			:param status: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(status)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:SPReemption {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.OsnmaTran:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TMODe \n
		Snippet: value: enums.OsnmaTran = driver.source.bb.gnss.galileo.osnma.get_tmode() \n
		Sets the OSNMA transition mode. These modes define the provision for the Public Key, TESLA chain and Alert Message. Also,
		the modes determine the OSNMA status transitions. \n
			:return: transition_mode: PRENewal| PREVocation| TRENewal| TREVocation| MRENewal| ALERt PRENewal Public key renewal mode PREVocation Public key revocation mode TRENewal TESLA chain renewal mode TREVocation TESLA chain revocation mode MRENewal Merkle tree renewal mode ALERt Alert message mode
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaTran)

	def set_tmode(self, transition_mode: enums.OsnmaTran) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TMODe \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_tmode(transition_mode = enums.OsnmaTran.ALERt) \n
		Sets the OSNMA transition mode. These modes define the provision for the Public Key, TESLA chain and Alert Message. Also,
		the modes determine the OSNMA status transitions. \n
			:param transition_mode: PRENewal| PREVocation| TRENewal| TREVocation| MRENewal| ALERt PRENewal Public key renewal mode PREVocation Public key revocation mode TRENewal TESLA chain renewal mode TREVocation TESLA chain revocation mode MRENewal Merkle tree renewal mode ALERt Alert message mode
		"""
		param = Conversions.enum_scalar_to_str(transition_mode, enums.OsnmaTran)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TMODe {param}')

	# noinspection PyTypeChecker
	def get_ts(self) -> enums.OsnmaTs:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TS \n
		Snippet: value: enums.OsnmaTs = driver.source.bb.gnss.galileo.osnma.get_ts() \n
		Sets the bits in the 4-bit Tag Size (TS) field. \n
			:return: value: 5| 6| 7| 8| 9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TS?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaTs)

	def set_ts(self, value: enums.OsnmaTs) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TS \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ts(value = enums.OsnmaTs._5) \n
		Sets the bits in the 4-bit Tag Size (TS) field. \n
			:param value: 5| 6| 7| 8| 9
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaTs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TS {param}')

	def clone(self) -> 'OsnmaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OsnmaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
