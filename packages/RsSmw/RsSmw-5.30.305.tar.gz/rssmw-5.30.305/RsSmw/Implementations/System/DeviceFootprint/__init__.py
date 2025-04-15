from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceFootprintCls:
	"""DeviceFootprint commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deviceFootprint", core, parent)

	@property
	def history(self):
		"""history commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_history'):
			from .History import HistoryCls
			self._history = HistoryCls(self._core, self._cmd_group)
		return self._history

	def set(self, directory: str) -> None:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: driver.system.deviceFootprint.set(directory = 'abc') \n
		Creates a file with the device footprint of the product. The content is formatted in machine-readable form, suitable for
		automatic further processing. The generic file name is composed of DeviceFootprint_<SerialNumber>_<Date>_<Time>.xml. R&S
		SMW200A saves the file in the definable directory. If the directory is not specified, it saves the footprint file in the
		internal default directory (/var/lib/Rohde-Schwarz/DeviceFootprint) . If you are obtaining technical support as described
		in 'Collecting information for technical support', this information is automatically retrieved and is part of the created
		*.tar.gz support file. You can download the file by using the SCPI commands of the MMEMory subsystem. \n
			:param directory: string Path to the directory for saving the device footprint file. Ensure that you have the permission to write into the directory.
		"""
		param = Conversions.value_to_quoted_str(directory)
		self._core.io.write(f'SYSTem:DFPRint {param}')

	def get(self) -> str:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: value: str = driver.system.deviceFootprint.get() \n
		Creates a file with the device footprint of the product. The content is formatted in machine-readable form, suitable for
		automatic further processing. The generic file name is composed of DeviceFootprint_<SerialNumber>_<Date>_<Time>.xml. R&S
		SMW200A saves the file in the definable directory. If the directory is not specified, it saves the footprint file in the
		internal default directory (/var/lib/Rohde-Schwarz/DeviceFootprint) . If you are obtaining technical support as described
		in 'Collecting information for technical support', this information is automatically retrieved and is part of the created
		*.tar.gz support file. You can download the file by using the SCPI commands of the MMEMory subsystem. \n
			:return: device_footprint: string Information on the product type, identification and the installed hardware, software and further service-related information on the product's configuration."""
		response = self._core.io.query_str(f'SYSTem:DFPRint?')
		return trim_str_response(response)

	def clone(self) -> 'DeviceFootprintCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DeviceFootprintCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
