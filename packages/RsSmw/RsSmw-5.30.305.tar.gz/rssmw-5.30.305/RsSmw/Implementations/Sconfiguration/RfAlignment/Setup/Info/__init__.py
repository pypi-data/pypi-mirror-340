from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InfoCls:
	"""Info commands group definition. 20 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("info", core, parent)

	@property
	def calibration(self):
		"""calibration commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def wiring(self):
		"""wiring commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_wiring'):
			from .Wiring import WiringCls
			self._wiring = WiringCls(self._core, self._cmd_group)
		return self._wiring

	# noinspection PyTypeChecker
	class DataStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Data_Type: str: No parameter help available
			- Setup_File: str: No parameter help available
			- Data_Value: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Data_Type'),
			ArgStruct.scalar_str('Setup_File'),
			ArgStruct.scalar_str('Data_Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Data_Type: str = None
			self.Setup_File: str = None
			self.Data_Value: str = None

	def get_data(self) -> DataStruct:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:DATA \n
		Snippet: value: DataStruct = driver.sconfiguration.rfAlignment.setup.info.get_data() \n
		No command help available \n
			:return: structure: for return value, see the help for DataStruct structure arguments.
		"""
		return self._core.io.query_struct('SCONfiguration:RFALignment:SETup:INFO:DATA?', self.__class__.DataStruct())

	def clone(self) -> 'InfoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InfoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
