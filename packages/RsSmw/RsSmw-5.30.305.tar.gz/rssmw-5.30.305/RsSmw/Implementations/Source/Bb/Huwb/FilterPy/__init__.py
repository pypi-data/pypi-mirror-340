from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 16 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def parameter(self):
		"""parameter commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .Parameter import ParameterCls
			self._parameter = ParameterCls(self._core, self._cmd_group)
		return self._parameter

	# noinspection PyTypeChecker
	def get_osampling(self) -> enums.HrpUwbOverSampling:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FILTer:OSAMpling \n
		Snippet: value: enums.HrpUwbOverSampling = driver.source.bb.huwb.filterPy.get_osampling() \n
		Sets the oversampling factor of the generated waveform. A reduced sample rate saves significantly the amount of memory or
		allows an increased signal cycle time, and vice versa. \n
			:return: oversampling: OS_1| OS_2| OS_3| OS_4| OS_5| OS_6| OS_7| OS_8 *RST: OS_1 (R&S SMW-K525) / OS_4 (R&S SMW-K527)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:OSAMpling?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbOverSampling)

	def set_osampling(self, oversampling: enums.HrpUwbOverSampling) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FILTer:OSAMpling \n
		Snippet: driver.source.bb.huwb.filterPy.set_osampling(oversampling = enums.HrpUwbOverSampling.OS_1) \n
		Sets the oversampling factor of the generated waveform. A reduced sample rate saves significantly the amount of memory or
		allows an increased signal cycle time, and vice versa. \n
			:param oversampling: OS_1| OS_2| OS_3| OS_4| OS_5| OS_6| OS_7| OS_8 *RST: OS_1 (R&S SMW-K525) / OS_4 (R&S SMW-K527)
		"""
		param = Conversions.enum_scalar_to_str(oversampling, enums.HrpUwbOverSampling)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:OSAMpling {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterHrpUwb:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FILTer:TYPE \n
		Snippet: value: enums.DmFilterHrpUwb = driver.source.bb.huwb.filterPy.get_type_py() \n
		Selects the baseband filter type. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| USER| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| APCO25Hcpm| APCO25Lsm| HRP| OQPSK
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterHrpUwb)

	def set_type_py(self, type_py: enums.DmFilterHrpUwb) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FILTer:TYPE \n
		Snippet: driver.source.bb.huwb.filterPy.set_type_py(type_py = enums.DmFilterHrpUwb.APCO25) \n
		Selects the baseband filter type. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| USER| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| APCO25Hcpm| APCO25Lsm| HRP| OQPSK
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterHrpUwb)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
