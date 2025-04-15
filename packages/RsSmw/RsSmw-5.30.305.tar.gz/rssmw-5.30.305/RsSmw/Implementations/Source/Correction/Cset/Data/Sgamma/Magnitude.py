from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MagnitudeCls:
	"""Magnitude commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("magnitude", core, parent)

	def set(self, magnitude_1: float, magnitude_n: float = None) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude \n
		Snippet: driver.source.correction.cset.data.sgamma.magnitude.set(magnitude_1 = 1.0, magnitude_n = 1.0) \n
		No command help available \n
			:param magnitude_1: No help available
			:param magnitude_n: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('magnitude_1', magnitude_1, DataType.Float), ArgSingle('magnitude_n', magnitude_n, DataType.Float, None, is_optional=True))
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude {param}'.rstrip())

	# noinspection PyTypeChecker
	class MagnitudeStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Magnitude_1: float: No parameter help available
			- 2 Magnitude_N: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Magnitude_1'),
			ArgStruct.scalar_float('Magnitude_N')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Magnitude_1: float = None
			self.Magnitude_N: float = None

	def get(self) -> MagnitudeStruct:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude \n
		Snippet: value: MagnitudeStruct = driver.source.correction.cset.data.sgamma.magnitude.get() \n
		No command help available \n
			:return: structure: for return value, see the help for MagnitudeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude?', self.__class__.MagnitudeStruct())

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude:POINts \n
		Snippet: value: int = driver.source.correction.cset.data.sgamma.magnitude.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude:POINts?')
		return Conversions.str_to_int(response)
