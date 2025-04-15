from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 12 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def parameter(self):
		"""parameter commands group. 2 Sub-classes, 7 commands."""
		if not hasattr(self, '_parameter'):
			from .Parameter import ParameterCls
			self._parameter = ParameterCls(self._core, self._cmd_group)
		return self._parameter

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilter:
		"""SCPI: [SOURce<HW>]:BB:DM:FILTer:TYPE \n
		Snippet: value: enums.DmFilter = driver.source.bb.dm.filterPy.get_type_py() \n
		Selects the filter type. If you select a standard (BB:DM:STAN) , the firmware automatically sets the standard-compliant
		filter type and filter parameter. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| USER| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| APCO25Hcpm| APCO25Lsm| HRP| SOQPSK
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilter)

	def set_type_py(self, type_py: enums.DmFilter) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:FILTer:TYPE \n
		Snippet: driver.source.bb.dm.filterPy.set_type_py(type_py = enums.DmFilter.APCO25) \n
		Selects the filter type. If you select a standard (BB:DM:STAN) , the firmware automatically sets the standard-compliant
		filter type and filter parameter. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| USER| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| APCO25Hcpm| APCO25Lsm| HRP| SOQPSK
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilter)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
