from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 14 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def ilength(self):
		"""ilength commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ilength'):
			from .Ilength import IlengthCls
			self._ilength = IlengthCls(self._core, self._cmd_group)
		return self._ilength

	@property
	def osampling(self):
		"""osampling commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_osampling'):
			from .Osampling import OsamplingCls
			self._osampling = OsamplingCls(self._core, self._cmd_group)
		return self._osampling

	@property
	def parameter(self):
		"""parameter commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_parameter'):
			from .Parameter import ParameterCls
			self._parameter = ParameterCls(self._core, self._cmd_group)
		return self._parameter

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterA:
		"""SCPI: [SOURce<HW>]:BB:WLAD:FILTer:TYPE \n
		Snippet: value: enums.DmFilterA = driver.source.bb.wlad.filterPy.get_type_py() \n
		Selects the filter type. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterA)

	def set_type_py(self, type_py: enums.DmFilterA) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:FILTer:TYPE \n
		Snippet: driver.source.bb.wlad.filterPy.set_type_py(type_py = enums.DmFilterA.APCO25) \n
		Selects the filter type. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterA)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
