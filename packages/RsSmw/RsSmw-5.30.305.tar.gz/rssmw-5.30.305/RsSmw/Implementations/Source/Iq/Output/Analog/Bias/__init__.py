from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BiasCls:
	"""Bias commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bias", core, parent)

	@property
	def coupling(self):
		"""coupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coupling'):
			from .Coupling import CouplingCls
			self._coupling = CouplingCls(self._core, self._cmd_group)
		return self._coupling

	def get_icomponent(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:I \n
		Snippet: value: float = driver.source.iq.output.analog.bias.get_icomponent() \n
		Sets the amplifier bias Vbias of the I component or Q component. To keep the I/Q analog output power levels below the
		maximum input power level at your DUT, see 'Maximum overall output voltage'. For more information, refer to the
		specifications document. \n
			:return: ipart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:I?')
		return Conversions.str_to_float(response)

	def set_icomponent(self, ipart: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:I \n
		Snippet: driver.source.iq.output.analog.bias.set_icomponent(ipart = 1.0) \n
		Sets the amplifier bias Vbias of the I component or Q component. To keep the I/Q analog output power levels below the
		maximum input power level at your DUT, see 'Maximum overall output voltage'. For more information, refer to the
		specifications document. \n
			:param ipart: float Range: (-4+Vp/2+Voffset/2) ,V to (4-Vp/2-Voffset/2) ,V (R&S SMW-B10) / -0.2V to 2.5V (R&S SMW-B9) , Unit: V
		"""
		param = Conversions.decimal_value_to_str(ipart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:I {param}')

	def get_qcomponent(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:Q \n
		Snippet: value: float = driver.source.iq.output.analog.bias.get_qcomponent() \n
		Sets the amplifier bias Vbias of the I component or Q component. To keep the I/Q analog output power levels below the
		maximum input power level at your DUT, see 'Maximum overall output voltage'. For more information, refer to the
		specifications document. \n
			:return: qpart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:Q?')
		return Conversions.str_to_float(response)

	def set_qcomponent(self, qpart: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:Q \n
		Snippet: driver.source.iq.output.analog.bias.set_qcomponent(qpart = 1.0) \n
		Sets the amplifier bias Vbias of the I component or Q component. To keep the I/Q analog output power levels below the
		maximum input power level at your DUT, see 'Maximum overall output voltage'. For more information, refer to the
		specifications document. \n
			:param qpart: float Range: (-4+Vp/2+Voffset/2) ,V to (4-Vp/2-Voffset/2) ,V (R&S SMW-B10) / -0.2V to 2.5V (R&S SMW-B9) , Unit: V
		"""
		param = Conversions.decimal_value_to_str(qpart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:Q {param}')

	def clone(self) -> 'BiasCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BiasCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
