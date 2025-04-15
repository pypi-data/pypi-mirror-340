from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 5 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_range'):
			from .Range import RangeCls
			self._range = RangeCls(self._core, self._cmd_group)
		return self._range

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.RfPortValType:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:FREQuency:MODE \n
		Snippet: value: enums.RfPortValType = driver.sconfiguration.rfAlignment.setup.info.calibration.frequency.get_mode() \n
		Queries the method used to be defined the calibrated frequency and PEP ranges. \n
			:return: mode: RANGe| LIST RANGe Range, see: method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Frequency.Range.lower method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Frequency.Range.upper method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Frequency.step method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Power.Range.lower method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Power.Range.upper method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Power.step LIST List, see: method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Frequency.ListPy.values method RsSmw.Sconfiguration.RfAlignment.Setup.Info.Calibration.Power.ListPy.values
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortValType)

	def get_step(self) -> float:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:FREQuency:STEP \n
		Snippet: value: float = driver.sconfiguration.rfAlignment.setup.info.calibration.frequency.get_step() \n
		Queries the frequency/PEP step size with that the calibration values are selected from the defined value range. \n
			:return: frequency_step: float
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:FREQuency:STEP?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FrequencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrequencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
