from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoefficientsCls:
	"""Coefficients commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coefficients", core, parent)

	def set(self, ipart_0: float, j_0: float, i_1: float, j_1: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SHAPing:POLYnomial:COEFficients \n
		Snippet: driver.source.iq.dpd.shaping.polynomial.coefficients.set(ipart_0 = 1.0, j_0 = 1.0, i_1 = 1.0, j_1 = 1.0) \n
		Sets the polynomial coefficients as a list of up to 10 comma separated value pairs. In Cartesian coordinates system, the
		coefficients bn are expressed in degrees. \n
			:param ipart_0: No help available
			:param j_0: float Range: -1E6 to 1E6
			:param i_1: No help available
			:param j_1: float Range: -1E6 to 1E6
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ipart_0', ipart_0, DataType.Float), ArgSingle('j_0', j_0, DataType.Float), ArgSingle('i_1', i_1, DataType.Float), ArgSingle('j_1', j_1, DataType.Float))
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:SHAPing:POLYnomial:COEFficients {param}'.rstrip())

	# noinspection PyTypeChecker
	class CoefficientsStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Ipart_0: float: No parameter help available
			- 2 J_0: float: float Range: -1E6 to 1E6
			- 3 I_1: float: No parameter help available
			- 4 J_1: float: float Range: -1E6 to 1E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ipart_0'),
			ArgStruct.scalar_float('J_0'),
			ArgStruct.scalar_float('I_1'),
			ArgStruct.scalar_float('J_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ipart_0: float = None
			self.J_0: float = None
			self.I_1: float = None
			self.J_1: float = None

	def get(self) -> CoefficientsStruct:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SHAPing:POLYnomial:COEFficients \n
		Snippet: value: CoefficientsStruct = driver.source.iq.dpd.shaping.polynomial.coefficients.get() \n
		Sets the polynomial coefficients as a list of up to 10 comma separated value pairs. In Cartesian coordinates system, the
		coefficients bn are expressed in degrees. \n
			:return: structure: for return value, see the help for CoefficientsStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:IQ:DPD:SHAPing:POLYnomial:COEFficients?', self.__class__.CoefficientsStruct())

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SHAPing:POLYnomial:COEFficients:CATalog \n
		Snippet: value: List[str] = driver.source.iq.dpd.shaping.polynomial.coefficients.get_catalog() \n
		Queries the available polynomial files in the default directory. Only files with the file extension *.dpd_poly are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:SHAPing:POLYnomial:COEFficients:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SHAPing:POLYnomial:COEFficients:LOAD \n
		Snippet: driver.source.iq.dpd.shaping.polynomial.coefficients.load(filename = 'abc') \n
		Loads the selected polynomial file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:SHAPing:POLYnomial:COEFficients:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SHAPing:POLYnomial:COEFficients:STORe \n
		Snippet: driver.source.iq.dpd.shaping.polynomial.coefficients.set_store(filename = 'abc') \n
		Saves the polynomial function as polynomial file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:SHAPing:POLYnomial:COEFficients:STORe {param}')
