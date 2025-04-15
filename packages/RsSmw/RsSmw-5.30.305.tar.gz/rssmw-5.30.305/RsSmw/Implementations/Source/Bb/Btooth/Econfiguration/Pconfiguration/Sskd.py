from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SskdCls:
	"""Sskd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sskd", core, parent)

	def set(self, sskd: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.sskd.set(sskd = rawAbc, bitcount = 1) \n
		Sets the portion of Central or the portion of the Peripheral of the session key diversifier (SKDm/SKDs) . \n
			:param sskd: numeric
			:param bitcount: integer Range: 64 to 64
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sskd', sskd, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD {param}'.rstrip())

	# noinspection PyTypeChecker
	class SskdStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Sskd: str: numeric
			- 2 Bitcount: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Sskd'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sskd: str = None
			self.Bitcount: int = None

	def get(self) -> SskdStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Snippet: value: SskdStruct = driver.source.bb.btooth.econfiguration.pconfiguration.sskd.get() \n
		Sets the portion of Central or the portion of the Peripheral of the session key diversifier (SKDm/SKDs) . \n
			:return: structure: for return value, see the help for SskdStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD?', self.__class__.SskdStruct())
