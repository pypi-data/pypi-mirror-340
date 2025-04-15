from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BextensionCls:
	"""Bextension commands group definition. 24 total commands, 5 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bextension", core, parent)

	@property
	def align(self):
		"""align commands group. 1 Sub-classes, 1 commands."""
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
	def correction(self):
		"""correction commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def info(self):
		"""info commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def setup(self):
		"""setup commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_setup'):
			from .Setup import SetupCls
			self._setup = SetupCls(self._core, self._cmd_group)
		return self._setup

	def get_dir(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:DIR \n
		Snippet: value: str = driver.sconfiguration.bextension.get_dir() \n
		No command help available \n
			:return: rem_dir: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:DIR?')
		return trim_str_response(response)

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:BEXTension:STATe \n
		Snippet: value: bool = driver.sconfiguration.bextension.get_state() \n
		Activates bandwidth extension. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SCONfiguration:BEXTension:STATe \n
		Snippet: driver.sconfiguration.bextension.set_state(state = False) \n
		Activates bandwidth extension. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SCONfiguration:BEXTension:STATe {param}')

	def clone(self) -> 'BextensionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BextensionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
