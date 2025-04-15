from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 16 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def ilength(self):
		"""ilength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ilength'):
			from .Ilength import IlengthCls
			self._ilength = IlengthCls(self._core, self._cmd_group)
		return self._ilength

	@property
	def osampling(self):
		"""osampling commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_osampling'):
			from .Osampling import OsamplingCls
			self._osampling = OsamplingCls(self._core, self._cmd_group)
		return self._osampling

	@property
	def parameter(self):
		"""parameter commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .Parameter import ParameterCls
			self._parameter = ParameterCls(self._core, self._cmd_group)
		return self._parameter

	def get_filters(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:FILTers \n
		Snippet: value: str = driver.source.bb.btooth.filterPy.get_filters() \n
		Queries all configured baseband filters. These filters are the common GFSK baseband filter and, for some EDR packets, a
		DPSK filter. See also Table 'DPSK filter for Bluetooth EDR packets'. \n
			:return: filters: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:FILTers?')
		return trim_str_response(response)

	def get_mindex(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:MINDex \n
		Snippet: value: str = driver.source.bb.btooth.filterPy.get_mindex() \n
		Queries the modulation index resulting from the entered frequency deviation value. \n
			:return: mindex: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:MINDex?')
		return trim_str_response(response)

	def get_mtype(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:MTYPe \n
		Snippet: value: str = driver.source.bb.btooth.filterPy.get_mtype() \n
		Queries the modulation type used for the current packet selection. \n
			:return: mtype: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:MTYPe?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:TYPE \n
		Snippet: value: enums.DmFilterB = driver.source.bb.btooth.filterPy.get_type_py() \n
		Selects the filters used for Pi/4 DQPSK and 8DPSK modulations. This opens a selection window containing all the filters
		available to the instrument. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterB)

	def set_type_py(self, type_py: enums.DmFilterB) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:FILTer:TYPE \n
		Snippet: driver.source.bb.btooth.filterPy.set_type_py(type_py = enums.DmFilterB.APCO25) \n
		Selects the filters used for Pi/4 DQPSK and 8DPSK modulations. This opens a selection window containing all the filters
		available to the instrument. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterB)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
