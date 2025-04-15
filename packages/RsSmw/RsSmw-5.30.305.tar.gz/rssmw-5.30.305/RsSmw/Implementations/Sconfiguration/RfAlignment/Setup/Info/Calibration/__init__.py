from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 16 total commands, 3 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def power(self):
		"""power commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def temperature(self):
		"""temperature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_temperature'):
			from .Temperature import TemperatureCls
			self._temperature = TemperatureCls(self._core, self._cmd_group)
		return self._temperature

	def get_age(self) -> int:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:AGE \n
		Snippet: value: int = driver.sconfiguration.rfAlignment.setup.info.calibration.get_age() \n
		Queries how many days are passed since the moment the calibration described in the loaded setup file is performed. \n
			:return: days: integer Time since calibration in days
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:AGE?')
		return Conversions.str_to_int(response)

	def get_date(self) -> str:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:DATE \n
		Snippet: value: str = driver.sconfiguration.rfAlignment.setup.info.calibration.get_date() \n
		Queries the time the calibration described in the loaded setup file is performed. \n
			:return: date: string
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:DATE?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_lo_coupling(self) -> enums.RfPortFreqMode:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:LOCoupling \n
		Snippet: value: enums.RfPortFreqMode = driver.sconfiguration.rfAlignment.setup.info.calibration.get_lo_coupling() \n
		Queries whether the instruments use a common local oscillator (LO) signal or not. \n
			:return: state: ACTive| NACTive ACTive All instruments are connected to the same LO reference frequency. NACTive Each instrument uses its own local oscillator.
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:LOCoupling?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortFreqMode)

	def get_parameters(self) -> str:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:PARameters \n
		Snippet: value: str = driver.sconfiguration.rfAlignment.setup.info.calibration.get_parameters() \n
		Queries information on the major calibrated parameters. \n
			:return: calibrated_param: string
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:PARameters?')
		return trim_str_response(response)

	def get_time(self) -> str:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:TIME \n
		Snippet: value: str = driver.sconfiguration.rfAlignment.setup.info.calibration.get_time() \n
		The date and time the calibration described in the loaded setup file is performed. \n
			:return: time: string
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:TIME?')
		return trim_str_response(response)

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
