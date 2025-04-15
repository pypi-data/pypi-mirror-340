from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqDelayCls:
	"""IqDelay commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqDelay", core, parent)

	@property
	def additional(self):
		"""additional commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_additional'):
			from .Additional import AdditionalCls
			self._additional = AdditionalCls(self._core, self._cmd_group)
		return self._additional

	def get(self, port=repcap.Port.Default) -> float:
		"""SCPI: SCONfiguration:BEXTension:CORRection:PORT<CH>:IQDelay \n
		Snippet: value: float = driver.sconfiguration.bextension.correction.port.iqDelay.get(port = repcap.Port.Default) \n
		Queries the IQ delay at the selected RF port. \n
			:param port: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Port')
			:return: ipart_qdelay: float"""
		port_cmd_val = self._cmd_group.get_repcap_cmd_value(port, repcap.Port)
		response = self._core.io.query_str(f'SCONfiguration:BEXTension:CORRection:PORT{port_cmd_val}:IQDelay?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'IqDelayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqDelayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
