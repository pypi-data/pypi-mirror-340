from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ProducerCls:
	"""Producer commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("producer", core, parent)

	def get_ip_address(self) -> bytes:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRODucer:IPADdress \n
		Snippet: value: bytes = driver.source.bb.arbitrary.producer.get_ip_address() \n
		No command help available \n
			:return: arb_producer_ip_address: No help available
		"""
		response = self._core.io.query_bin_block('SOURce<HwInstance>:BB:ARBitrary:PRODucer:IPADdress?')
		return response

	def set_ip_address(self, arb_producer_ip_address: bytes) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRODucer:IPADdress \n
		Snippet: driver.source.bb.arbitrary.producer.set_ip_address(arb_producer_ip_address = b'ABCDEFGH') \n
		No command help available \n
			:param arb_producer_ip_address: No help available
		"""
		self._core.io.write_bin_block('SOURce<HwInstance>:BB:ARBitrary:PRODucer:IPADdress ', arb_producer_ip_address)

	def get_port(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRODucer:PORT \n
		Snippet: value: int = driver.source.bb.arbitrary.producer.get_port() \n
		No command help available \n
			:return: port: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:PRODucer:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, port: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRODucer:PORT \n
		Snippet: driver.source.bb.arbitrary.producer.set_port(port = 1) \n
		No command help available \n
			:param port: No help available
		"""
		param = Conversions.decimal_value_to_str(port)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:PRODucer:PORT {param}')
