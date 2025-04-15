from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ParameterCls:
	"""Parameter commands group definition. 14 total commands, 2 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("parameter", core, parent)

	@property
	def cosine(self):
		"""cosine commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cosine'):
			from .Cosine import CosineCls
			self._cosine = CosineCls(self._core, self._cmd_group)
		return self._cosine

	@property
	def lte(self):
		"""lte commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_lte'):
			from .Lte import LteCls
			self._lte = LteCls(self._core, self._cmd_group)
		return self._lte

	def get_apco_25(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:APCO25 \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_apco_25() \n
		No command help available \n
			:return: apco_25: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:APCO25 \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_apco_25(apco_25 = 1.0) \n
		No command help available \n
			:param apco_25: No help available
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:APCO25 {param}')

	def get_gauss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:GAUSs \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_gauss() \n
		No command help available \n
			:return: gauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:GAUSs \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_gauss(gauss = 1.0) \n
		No command help available \n
			:param gauss: No help available
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:LPASSEVM \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_lpass_evm() \n
		No command help available \n
			:return: cutoff_frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, cutoff_frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:LPASSEVM \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_lpass_evm(cutoff_frequency = 1.0) \n
		No command help available \n
			:param cutoff_frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(cutoff_frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:LPASs \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_lpass() \n
		No command help available \n
			:return: lpass: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:LPASs \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_lpass(lpass = 1.0) \n
		No command help available \n
			:param lpass: No help available
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:PGAuss \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_pgauss() \n
		No command help available \n
			:return: pgauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:PGAuss \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_pgauss(pgauss = 1.0) \n
		No command help available \n
			:param pgauss: No help available
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:RCOSine \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_rcosine() \n
		No command help available \n
			:return: rcosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:RCOSine \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_rcosine(rcosine = 1.0) \n
		No command help available \n
			:param rcosine: No help available
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:SPHase \n
		Snippet: value: float = driver.source.bb.v5G.filterPy.parameter.get_sphase() \n
		No command help available \n
			:return: sphase: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:SPHase \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_sphase(sphase = 1.0) \n
		No command help available \n
			:param sphase: No help available
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:SPHase {param}')

	def get_user(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:USER \n
		Snippet: value: str = driver.source.bb.v5G.filterPy.parameter.get_user() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:V5G:FILTer:PARameter:USER?')
		return trim_str_response(response)

	def set_user(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:FILTer:PARameter:USER \n
		Snippet: driver.source.bb.v5G.filterPy.parameter.set_user(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:FILTer:PARameter:USER {param}')

	def clone(self) -> 'ParameterCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ParameterCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
