from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfAlignmentCls:
	"""RfAlignment commands group definition. 29 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfAlignment", core, parent)

	@property
	def align(self):
		"""align commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_align'):
			from .Align import AlignCls
			self._align = AlignCls(self._core, self._cmd_group)
		return self._align

	@property
	def calibration(self):
		"""calibration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def qcheck(self):
		"""qcheck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qcheck'):
			from .Qcheck import QcheckCls
			self._qcheck = QcheckCls(self._core, self._cmd_group)
		return self._qcheck

	@property
	def setup(self):
		"""setup commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_setup'):
			from .Setup import SetupCls
			self._setup = SetupCls(self._core, self._cmd_group)
		return self._setup

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:RFALignment:STATe \n
		Snippet: value: bool = driver.sconfiguration.rfAlignment.get_state() \n
		If a valid setup file is selected, applies the specified correction data. Load the setup file with the command method
		RsSmw.Sconfiguration.RfAlignment.Setup.File.value. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SCONfiguration:RFALignment:STATe \n
		Snippet: driver.sconfiguration.rfAlignment.set_state(state = False) \n
		If a valid setup file is selected, applies the specified correction data. Load the setup file with the command method
		RsSmw.Sconfiguration.RfAlignment.Setup.File.value. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SCONfiguration:RFALignment:STATe {param}')

	def clone(self) -> 'RfAlignmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfAlignmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
