from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EsCls:
	"""Es commands group definition. 7 total commands, 2 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("es", core, parent)

	@property
	def cs(self):
		"""cs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs'):
			from .Cs import CsCls
			self._cs = CsCls(self._core, self._cmd_group)
		return self._cs

	@property
	def tp(self):
		"""tp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp'):
			from .Tp import TpCls
			self._tp = TpCls(self._core, self._cmd_group)
		return self._tp

	def get_cs_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:CSLength \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.general.es.get_cs_length() \n
		Sets the number of symbols in the CORESET. \n
			:return: qck_set_corset_len: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:CSLength?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_mod(self) -> enums.QckSettingsModType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:MOD \n
		Snippet: value: enums.QckSettingsModType = driver.source.bb.nr5G.qckset.general.es.get_mod() \n
		Sets the modulation scheme. \n
			:return: qck_set_mod_type: QPSK| QAM16| QAM64| QAM256| BPSK2| QAM1024
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:MOD?')
		return Conversions.str_to_scalar_enum(response, enums.QckSettingsModType)

	def set_mod(self, qck_set_mod_type: enums.QckSettingsModType) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:MOD \n
		Snippet: driver.source.bb.nr5G.qckset.general.es.set_mod(qck_set_mod_type = enums.QckSettingsModType.BPSK2) \n
		Sets the modulation scheme. \n
			:param qck_set_mod_type: QPSK| QAM16| QAM64| QAM256| BPSK2| QAM1024
		"""
		param = Conversions.enum_scalar_to_str(qck_set_mod_type, enums.QckSettingsModType)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:MOD {param}')

	# noinspection PyTypeChecker
	def get_rb_config(self) -> enums.Config:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBConfig \n
		Snippet: value: enums.Config = driver.source.bb.nr5G.qckset.general.es.get_rb_config() \n
		Sets the configuration mode for the resource block configuration. \n
			:return: qck_set_rb_config: MAN| EFL| EFR| ERL| ERR| OUTF| INNF| I1RL| I1RR| OUTP| O1RL| O1RR| R1IF| R1IL| R1IR| R2IF| R2IL| R2IR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBConfig?')
		return Conversions.str_to_scalar_enum(response, enums.Config)

	def set_rb_config(self, qck_set_rb_config: enums.Config) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBConfig \n
		Snippet: driver.source.bb.nr5G.qckset.general.es.set_rb_config(qck_set_rb_config = enums.Config.EFL) \n
		Sets the configuration mode for the resource block configuration. \n
			:param qck_set_rb_config: MAN| EFL| EFR| ERL| ERR| OUTF| INNF| I1RL| I1RR| OUTP| O1RL| O1RR| R1IF| R1IL| R1IR| R2IF| R2IL| R2IR
		"""
		param = Conversions.enum_scalar_to_str(qck_set_rb_config, enums.Config)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBConfig {param}')

	def get_rb_number(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBNumber \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.general.es.get_rb_number() \n
		Sets the number of resource blocks. \n
			:return: qck_set_rb_num: integer Range: 1 to 273
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBNumber?')
		return Conversions.str_to_int(response)

	def get_rb_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.general.es.get_rb_offset() \n
		Sets the resource block offset. \n
			:return: qck_set_rb_offset: integer Range: 0 to 272
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBOFfset?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'EsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
