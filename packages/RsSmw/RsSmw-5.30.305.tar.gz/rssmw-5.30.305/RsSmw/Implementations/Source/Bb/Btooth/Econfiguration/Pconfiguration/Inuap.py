from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InuapCls:
	"""Inuap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inuap", core, parent)

	def set(self, nap_uap: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.inuap.set(nap_uap = rawAbc, bitcount = 1) \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner's or initiator's target device address to which the advertisement is
		directed ..:TNUap. \n
			:param nap_uap: numeric
			:param bitcount: integer Range: 24 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('nap_uap', nap_uap, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap {param}'.rstrip())

	# noinspection PyTypeChecker
	class InuapStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Nap_Uap: str: numeric
			- 2 Bitcount: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Nap_Uap'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: str = None
			self.Bitcount: int = None

	def get(self) -> InuapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Snippet: value: InuapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.inuap.get() \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner's or initiator's target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for InuapStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap?', self.__class__.InuapStruct())
