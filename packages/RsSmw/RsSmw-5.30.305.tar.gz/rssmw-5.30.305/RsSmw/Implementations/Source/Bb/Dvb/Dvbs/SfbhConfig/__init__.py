from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfbhConfigCls:
	"""SfbhConfig commands group definition. 10 total commands, 2 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfbhConfig", core, parent)

	@property
	def dt(self):
		"""dt commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dt'):
			from .Dt import DtCls
			self._dt = DtCls(self._core, self._cmd_group)
		return self._dt

	@property
	def fodt(self):
		"""fodt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fodt'):
			from .Fodt import FodtCls
			self._fodt = FodtCls(self._core, self._cmd_group)
		return self._fodt

	def get_ao_dwell(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:AODWell \n
		Snippet: value: bool = driver.source.bb.dvb.dvbs.sfbhConfig.get_ao_dwell() \n
		Activates the attenuation of dwells DT1 to DT9. \n
			:return: attenuate_oth_dw: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:AODWell?')
		return Conversions.str_to_bool(response)

	def set_ao_dwell(self, attenuate_oth_dw: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:AODWell \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_ao_dwell(attenuate_oth_dw = False) \n
		Activates the attenuation of dwells DT1 to DT9. \n
			:param attenuate_oth_dw: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(attenuate_oth_dw)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:AODWell {param}')

	def get_bh_cycle(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:BHCycle \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfbhConfig.get_bh_cycle() \n
		Displays the beam hopping cycle that is the cumulative result of all dwells length. \n
			:return: bh_cycle: integer Range: 0 to 2047974660
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:BHCycle?')
		return Conversions.str_to_int(response)

	def get_bs_time(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:BSTime \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfbhConfig.get_bs_time() \n
		Sets the beam switching time. \n
			:return: beam_switch_time: integer Range: 1 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:BSTime?')
		return Conversions.str_to_int(response)

	def set_bs_time(self, beam_switch_time: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:BSTime \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_bs_time(beam_switch_time = 1) \n
		Sets the beam switching time. \n
			:param beam_switch_time: integer Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(beam_switch_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:BSTime {param}')

	def get_lsf_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:LSFLength \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfbhConfig.get_lsf_length() \n
		Queries the length of the last super frame. \n
			:return: last_sf_length: integer Range: 8856 to 612540
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:LSFLength?')
		return Conversions.str_to_int(response)

	def get_no_dwells(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:NODWells \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfbhConfig.get_no_dwells() \n
		Sets the number of dwells. \n
			:return: number_of_dwells: integer Range: 1 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:NODWells?')
		return Conversions.str_to_int(response)

	def set_no_dwells(self, number_of_dwells: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:NODWells \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_no_dwells(number_of_dwells = 1) \n
		Sets the number of dwells. \n
			:param number_of_dwells: integer Range: 1 to 10
		"""
		param = Conversions.decimal_value_to_str(number_of_dwells)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:NODWells {param}')

	def get_nosf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:NOSF \n
		Snippet: value: int = driver.source.bb.dvb.dvbs.sfbhConfig.get_nosf() \n
		Sets the number of super frames. \n
			:return: number_of_sf: integer Range: 1 to 25
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:NOSF?')
		return Conversions.str_to_int(response)

	def set_nosf(self, number_of_sf: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:NOSF \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_nosf(number_of_sf = 1) \n
		Sets the number of super frames. \n
			:param number_of_sf: integer Range: 1 to 25
		"""
		param = Conversions.decimal_value_to_str(number_of_sf)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:NOSF {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:STATe \n
		Snippet: value: bool = driver.source.bb.dvb.dvbs.sfbhConfig.get_state() \n
		Activates the beam hopping. \n
			:return: beam_hopping_stat: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, beam_hopping_stat: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:STATe \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_state(beam_hopping_stat = False) \n
		Activates the beam hopping. \n
			:param beam_hopping_stat: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(beam_hopping_stat)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:STATe {param}')

	def get_zbs_signal(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:ZBSSignal \n
		Snippet: value: bool = driver.source.bb.dvb.dvbs.sfbhConfig.get_zbs_signal() \n
		Activates the switching signal for zero beam state. \n
			:return: zero_beam_switch: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:ZBSSignal?')
		return Conversions.str_to_bool(response)

	def set_zbs_signal(self, zero_beam_switch: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBS:SFBHconfig:ZBSSignal \n
		Snippet: driver.source.bb.dvb.dvbs.sfbhConfig.set_zbs_signal(zero_beam_switch = False) \n
		Activates the switching signal for zero beam state. \n
			:param zero_beam_switch: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(zero_beam_switch)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBS:SFBHconfig:ZBSSignal {param}')

	def clone(self) -> 'SfbhConfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SfbhConfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
