from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserPattCls:
	"""UserPatt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("userPatt", core, parent)

	def set(self, user_patt: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.userPatt.set(user_patt = rawAbc, bitcount = 1) \n
		Sets a user-defined pattern of the 32-bit Sync Word. Using this Sync Word requires the following setting:
		SOURce1:BB:BTOoth:ECONfiguration:PCONfiguration:SYNCword UPAT \n
			:param user_patt: numeric
			:param bitcount: integer Range: 1 to 32
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('user_patt', user_patt, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt {param}'.rstrip())

	# noinspection PyTypeChecker
	class UserPattStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 User_Patt: str: numeric
			- 2 Bitcount: int: integer Range: 1 to 32"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('User_Patt'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.User_Patt: str = None
			self.Bitcount: int = None

	def get(self) -> UserPattStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt \n
		Snippet: value: UserPattStruct = driver.source.bb.btooth.econfiguration.pconfiguration.userPatt.get() \n
		Sets a user-defined pattern of the 32-bit Sync Word. Using this Sync Word requires the following setting:
		SOURce1:BB:BTOoth:ECONfiguration:PCONfiguration:SYNCword UPAT \n
			:return: structure: for return value, see the help for UserPattStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt?', self.__class__.UserPattStruct())
