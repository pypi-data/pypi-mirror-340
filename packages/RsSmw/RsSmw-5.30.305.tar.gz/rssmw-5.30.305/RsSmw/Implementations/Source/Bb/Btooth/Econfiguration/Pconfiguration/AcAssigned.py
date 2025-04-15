from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcAssignedCls:
	"""AcAssigned commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acAssigned", core, parent)

	def set(self, ac_assigned: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.acAssigned.set(ac_assigned = rawAbc, bitcount = 1) \n
		Sets the advertiser's device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param ac_assigned: numeric
			:param bitcount: integer Range: 24 to 24
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ac_assigned', ac_assigned, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned {param}'.rstrip())

	# noinspection PyTypeChecker
	class AcAssignedStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ac_Assigned: str: No parameter help available
			- 2 Bitcount: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Ac_Assigned'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ac_Assigned: str = None
			self.Bitcount: int = None

	def get(self) -> AcAssignedStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Snippet: value: AcAssignedStruct = driver.source.bb.btooth.econfiguration.pconfiguration.acAssigned.get() \n
		Sets the advertiser's device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for AcAssignedStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned?', self.__class__.AcAssignedStruct())
