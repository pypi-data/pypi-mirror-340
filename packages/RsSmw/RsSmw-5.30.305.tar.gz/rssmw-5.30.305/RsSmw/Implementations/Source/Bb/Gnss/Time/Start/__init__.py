from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartCls:
	"""Start commands group definition. 42 total commands, 12 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def galileo(self):
		"""galileo commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Sbas import SbasCls
			self._sbas = SbasCls(self._core, self._cmd_group)
		return self._sbas

	@property
	def scTime(self):
		"""scTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scTime'):
			from .ScTime import ScTimeCls
			self._scTime = ScTimeCls(self._core, self._cmd_group)
		return self._scTime

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def utc(self):
		"""utc commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_utc'):
			from .Utc import UtcCls
			self._utc = UtcCls(self._core, self._cmd_group)
		return self._utc

	@property
	def xona(self):
		"""xona commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_xona'):
			from .Xona import XonaCls
			self._xona = XonaCls(self._core, self._cmd_group)
		return self._xona

	# noinspection PyTypeChecker
	def get_tbasis(self) -> enums.TimeBasis:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:TBASis \n
		Snippet: value: enums.TimeBasis = driver.source.bb.gnss.time.start.get_tbasis() \n
		Sets the timebase to enter the simulation start time. This timebase is also the timebase for assistance data generation,
		see [:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis?. \n
			:return: system_time: UTC| GPS| GST| GLO| BDT| NAV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TBASis?')
		return Conversions.str_to_scalar_enum(response, enums.TimeBasis)

	def set_tbasis(self, system_time: enums.TimeBasis) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:TBASis \n
		Snippet: driver.source.bb.gnss.time.start.set_tbasis(system_time = enums.TimeBasis.BDT) \n
		Sets the timebase to enter the simulation start time. This timebase is also the timebase for assistance data generation,
		see [:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis?. \n
			:param system_time: UTC| GPS| GST| GLO| BDT| NAV
		"""
		param = Conversions.enum_scalar_to_str(system_time, enums.TimeBasis)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:TBASis {param}')

	def get_to_week(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:TOWeek \n
		Snippet: value: float = driver.source.bb.gnss.time.start.get_to_week() \n
		If time base is GPS or GST, sets the simulation start time within week set with the command
		[:SOURce<hw>]:BB:GNSS:TIME:STARt:WNUMber. \n
			:return: tow: float Number of seconds since the beginning of the week Range: 0 to 604799.999
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TOWeek?')
		return Conversions.str_to_float(response)

	def set_to_week(self, tow: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:TOWeek \n
		Snippet: driver.source.bb.gnss.time.start.set_to_week(tow = 1.0) \n
		If time base is GPS or GST, sets the simulation start time within week set with the command
		[:SOURce<hw>]:BB:GNSS:TIME:STARt:WNUMber. \n
			:param tow: float Number of seconds since the beginning of the week Range: 0 to 604799.999
		"""
		param = Conversions.decimal_value_to_str(tow)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:TOWeek {param}')

	def get_wnumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:WNUMber \n
		Snippet: value: int = driver.source.bb.gnss.time.start.get_wnumber() \n
		If time base is GPS or GST, sets the week number (WN) . \n
			:return: week: integer The weeks are numbered starting from a reference time point (WN_REF=0) , that depends on the navigation standard. Range: 0 to 9999*53
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:WNUMber?')
		return Conversions.str_to_int(response)

	def set_wnumber(self, week: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:WNUMber \n
		Snippet: driver.source.bb.gnss.time.start.set_wnumber(week = 1) \n
		If time base is GPS or GST, sets the week number (WN) . \n
			:param week: integer The weeks are numbered starting from a reference time point (WN_REF=0) , that depends on the navigation standard. Range: 0 to 9999*53
		"""
		param = Conversions.decimal_value_to_str(week)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:WNUMber {param}')

	def clone(self) -> 'StartCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StartCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
