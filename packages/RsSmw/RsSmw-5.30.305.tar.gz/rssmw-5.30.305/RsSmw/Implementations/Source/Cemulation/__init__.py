from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CemulationCls:
	"""Cemulation commands group definition. 733 total commands, 28 Subgroups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cemulation", core, parent)

	@property
	def birthDeath(self):
		"""birthDeath commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_birthDeath'):
			from .BirthDeath import BirthDeathCls
			self._birthDeath = BirthDeathCls(self._core, self._cmd_group)
		return self._birthDeath

	@property
	def bypass(self):
		"""bypass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bypass'):
			from .Bypass import BypassCls
			self._bypass = BypassCls(self._core, self._cmd_group)
		return self._bypass

	@property
	def cdynamic(self):
		"""cdynamic commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_cdynamic'):
			from .Cdynamic import CdynamicCls
			self._cdynamic = CdynamicCls(self._core, self._cmd_group)
		return self._cdynamic

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def copy(self):
		"""copy commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_copy'):
			from .Copy import CopyCls
			self._copy = CopyCls(self._core, self._cmd_group)
		return self._copy

	@property
	def couple(self):
		"""couple commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_couple'):
			from .Couple import CoupleCls
			self._couple = CoupleCls(self._core, self._cmd_group)
		return self._couple

	@property
	def delPy(self):
		"""delPy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_delPy'):
			from .DelPy import DelPyCls
			self._delPy = DelPyCls(self._core, self._cmd_group)
		return self._delPy

	@property
	def delay(self):
		"""delay commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def doppler(self):
		"""doppler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_doppler'):
			from .Doppler import DopplerCls
			self._doppler = DopplerCls(self._core, self._cmd_group)
		return self._doppler

	@property
	def dsSimulation(self):
		"""dsSimulation commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_dsSimulation'):
			from .DsSimulation import DsSimulationCls
			self._dsSimulation = DsSimulationCls(self._core, self._cmd_group)
		return self._dsSimulation

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def globale(self):
		"""globale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_globale'):
			from .Globale import GlobaleCls
			self._globale = GlobaleCls(self._core, self._cmd_group)
		return self._globale

	@property
	def hopping(self):
		"""hopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopping'):
			from .Hopping import HoppingCls
			self._hopping = HoppingCls(self._core, self._cmd_group)
		return self._hopping

	@property
	def hsTrain(self):
		"""hsTrain commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_hsTrain'):
			from .HsTrain import HsTrainCls
			self._hsTrain = HsTrainCls(self._core, self._cmd_group)
		return self._hsTrain

	@property
	def ignore(self):
		"""ignore commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ignore'):
			from .Ignore import IgnoreCls
			self._ignore = IgnoreCls(self._core, self._cmd_group)
		return self._ignore

	@property
	def iloss(self):
		"""iloss commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_iloss'):
			from .Iloss import IlossCls
			self._iloss = IlossCls(self._core, self._cmd_group)
		return self._iloss

	@property
	def mdelay(self):
		"""mdelay commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_mdelay'):
			from .Mdelay import MdelayCls
			self._mdelay = MdelayCls(self._core, self._cmd_group)
		return self._mdelay

	@property
	def mimo(self):
		"""mimo commands group. 6 Sub-classes, 6 commands."""
		if not hasattr(self, '_mimo'):
			from .Mimo import MimoCls
			self._mimo = MimoCls(self._core, self._cmd_group)
		return self._mimo

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_restart'):
			from .Restart import RestartCls
			self._restart = RestartCls(self._core, self._cmd_group)
		return self._restart

	@property
	def scm(self):
		"""scm commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_scm'):
			from .Scm import ScmCls
			self._scm = ScmCls(self._core, self._cmd_group)
		return self._scm

	@property
	def siso(self):
		"""siso commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_siso'):
			from .Siso import SisoCls
			self._siso = SisoCls(self._core, self._cmd_group)
		return self._siso

	@property
	def speed(self):
		"""speed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speed'):
			from .Speed import SpeedCls
			self._speed = SpeedCls(self._core, self._cmd_group)
		return self._speed

	@property
	def standard(self):
		"""standard commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_standard'):
			from .Standard import StandardCls
			self._standard = StandardCls(self._core, self._cmd_group)
		return self._standard

	@property
	def sum(self):
		"""sum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sum'):
			from .Sum import SumCls
			self._sum = SumCls(self._core, self._cmd_group)
		return self._sum

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .Synchronize import SynchronizeCls
			self._synchronize = SynchronizeCls(self._core, self._cmd_group)
		return self._synchronize

	@property
	def tcInterferer(self):
		"""tcInterferer commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_tcInterferer'):
			from .TcInterferer import TcInterfererCls
			self._tcInterferer = TcInterfererCls(self._core, self._cmd_group)
		return self._tcInterferer

	@property
	def test(self):
		"""test commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:CEMulation:CATalog \n
		Snippet: value: List[str] = driver.source.cemulation.get_catalog() \n
		No command help available \n
			:return: filenames: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CATalog?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_configuration(self) -> enums.FadType:
		"""SCPI: [SOURce<HW>]:CEMulation:CONFiguration \n
		Snippet: value: enums.FadType = driver.source.cemulation.get_configuration() \n
		No command help available \n
			:return: configuration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CONFiguration?')
		return Conversions.str_to_scalar_enum(response, enums.FadType)

	def set_configuration(self, configuration: enums.FadType) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:CONFiguration \n
		Snippet: driver.source.cemulation.set_configuration(configuration = enums.FadType.BIRThdeath) \n
		No command help available \n
			:param configuration: No help available
		"""
		param = Conversions.enum_scalar_to_str(configuration, enums.FadType)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:CONFiguration {param}')

	def get_cspeed(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:CSPeed \n
		Snippet: value: bool = driver.source.cemulation.get_cspeed() \n
		No command help available \n
			:return: cspeed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:CSPeed?')
		return Conversions.str_to_bool(response)

	def set_cspeed(self, cspeed: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:CSPeed \n
		Snippet: driver.source.cemulation.set_cspeed(cspeed = False) \n
		No command help available \n
			:param cspeed: No help available
		"""
		param = Conversions.bool_to_str(cspeed)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:CSPeed {param}')

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:DELETE \n
		Snippet: driver.source.cemulation.delete(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:DELETE {param}')

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.FadPathFiltAll:
		"""SCPI: [SOURce<HW>]:CEMulation:FILTer \n
		Snippet: value: enums.FadPathFiltAll = driver.source.cemulation.get_filter_py() \n
		No command help available \n
			:return: path_filter: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.FadPathFiltAll)

	def set_filter_py(self, path_filter: enums.FadPathFiltAll) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:FILTer \n
		Snippet: driver.source.cemulation.set_filter_py(path_filter = enums.FadPathFiltAll.ACTPlus) \n
		No command help available \n
			:param path_filter: No help available
		"""
		param = Conversions.enum_scalar_to_str(path_filter, enums.FadPathFiltAll)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:FILTer {param}')

	# noinspection PyTypeChecker
	def get_kconstant(self) -> enums.FadKeepConst:
		"""SCPI: [SOURce<HW>]:CEMulation:KCONstant \n
		Snippet: value: enums.FadKeepConst = driver.source.cemulation.get_kconstant() \n
		No command help available \n
			:return: kconstant: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:KCONstant?')
		return Conversions.str_to_scalar_enum(response, enums.FadKeepConst)

	def set_kconstant(self, kconstant: enums.FadKeepConst) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:KCONstant \n
		Snippet: driver.source.cemulation.set_kconstant(kconstant = enums.FadKeepConst.DSHift) \n
		No command help available \n
			:param kconstant: No help available
		"""
		param = Conversions.enum_scalar_to_str(kconstant, enums.FadKeepConst)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:KCONstant {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:LOAD \n
		Snippet: driver.source.cemulation.load(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:LOAD {param}')

	def get_plength(self) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:PLENgth \n
		Snippet: value: float = driver.source.cemulation.get_plength() \n
		No command help available \n
			:return: fsim_path_length: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:PLENgth?')
		return Conversions.str_to_float(response)

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:PRESet \n
		Snippet: driver.source.cemulation.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:PRESet \n
		Snippet: driver.source.cemulation.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CEMulation:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_route(self) -> enums.FadConfPathOut:
		"""SCPI: [SOURce<HW>]:CEMulation:ROUTe \n
		Snippet: value: enums.FadConfPathOut = driver.source.cemulation.get_route() \n
		No command help available \n
			:return: route: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.FadConfPathOut)

	def set_route(self, route: enums.FadConfPathOut) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:ROUTe \n
		Snippet: driver.source.cemulation.set_route(route = enums.FadConfPathOut.FA1A2BFB1A2B) \n
		No command help available \n
			:param route: No help available
		"""
		param = Conversions.enum_scalar_to_str(route, enums.FadConfPathOut)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:ROUTe {param}')

	# noinspection PyTypeChecker
	def get_sdestination(self) -> enums.FadSignDest:
		"""SCPI: [SOURce<HW>]:CEMulation:SDEStination \n
		Snippet: value: enums.FadSignDest = driver.source.cemulation.get_sdestination() \n
		No command help available \n
			:return: sdestination: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:SDEStination?')
		return Conversions.str_to_scalar_enum(response, enums.FadSignDest)

	def set_sdestination(self, sdestination: enums.FadSignDest) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SDEStination \n
		Snippet: driver.source.cemulation.set_sdestination(sdestination = enums.FadSignDest.BB) \n
		No command help available \n
			:param sdestination: No help available
		"""
		param = Conversions.enum_scalar_to_str(sdestination, enums.FadSignDest)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SDEStination {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:STORe \n
		Snippet: driver.source.cemulation.set_store(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:STORe {param}')

	# noinspection PyTypeChecker
	def get_tpreset(self) -> enums.FadTablePreset:
		"""SCPI: [SOURce<HW>]:CEMulation:TPREset \n
		Snippet: value: enums.FadTablePreset = driver.source.cemulation.get_tpreset() \n
		No command help available \n
			:return: preset_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:TPREset?')
		return Conversions.str_to_scalar_enum(response, enums.FadTablePreset)

	def set_tpreset(self, preset_type: enums.FadTablePreset) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:TPREset \n
		Snippet: driver.source.cemulation.set_tpreset(preset_type = enums.FadTablePreset.LOS) \n
		No command help available \n
			:param preset_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(preset_type, enums.FadTablePreset)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:TPREset {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CEMulation:[STATe] \n
		Snippet: value: bool = driver.source.cemulation.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:[STATe] \n
		Snippet: driver.source.cemulation.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:STATe {param}')

	def clone(self) -> 'CemulationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CemulationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
