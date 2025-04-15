from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LtKeyCls:
	"""LtKey commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ltKey", core, parent)

	def set(self, lt_key: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:LTKey \n
		Snippet: driver.source.bb.btooth.econfiguration.ltKey.set(lt_key = rawAbc, bitcount = 1) \n
		Indicates the time the controller needs to receive the long-term key from the host. After this time, the controller is
		ready to enter into the last phase of encryption mode setup. \n
			:param lt_key: numeric
			:param bitcount: integer Range: 128 to 128
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lt_key', lt_key, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:LTKey {param}'.rstrip())

	# noinspection PyTypeChecker
	class LtKeyStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Lt_Key: str: numeric
			- 2 Bitcount: int: integer Range: 128 to 128"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Lt_Key'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lt_Key: str = None
			self.Bitcount: int = None

	def get(self) -> LtKeyStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:LTKey \n
		Snippet: value: LtKeyStruct = driver.source.bb.btooth.econfiguration.ltKey.get() \n
		Indicates the time the controller needs to receive the long-term key from the host. After this time, the controller is
		ready to enter into the last phase of encryption mode setup. \n
			:return: structure: for return value, see the help for LtKeyStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:LTKey?', self.__class__.LtKeyStruct())
