from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StreamCls:
	"""Stream commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stream", core, parent)

	@property
	def errors(self):
		"""errors commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_errors'):
			from .Errors import ErrorsCls
			self._errors = ErrorsCls(self._core, self._cmd_group)
		return self._errors

	@property
	def rxbLive(self):
		"""rxbLive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxbLive'):
			from .RxbLive import RxbLiveCls
			self._rxbLive = RxbLiveCls(self._core, self._cmd_group)
		return self._rxbLive

	@property
	def rxbMin(self):
		"""rxbMin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxbMin'):
			from .RxbMin import RxbMinCls
			self._rxbMin = RxbMinCls(self._core, self._cmd_group)
		return self._rxbMin

	@property
	def rxcFrames(self):
		"""rxcFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxcFrames'):
			from .RxcFrames import RxcFramesCls
			self._rxcFrames = RxcFramesCls(self._core, self._cmd_group)
		return self._rxcFrames

	@property
	def rxdBytes(self):
		"""rxdBytes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxdBytes'):
			from .RxdBytes import RxdBytesCls
			self._rxdBytes = RxdBytesCls(self._core, self._cmd_group)
		return self._rxdBytes

	@property
	def rxdFrames(self):
		"""rxdFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxdFrames'):
			from .RxdFrames import RxdFramesCls
			self._rxdFrames = RxdFramesCls(self._core, self._cmd_group)
		return self._rxdFrames

	@property
	def rxuSegments(self):
		"""rxuSegments commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxuSegments'):
			from .RxuSegments import RxuSegmentsCls
			self._rxuSegments = RxuSegmentsCls(self._core, self._cmd_group)
		return self._rxuSegments

	@property
	def txrFrames(self):
		"""txrFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txrFrames'):
			from .TxrFrames import TxrFramesCls
			self._txrFrames = TxrFramesCls(self._core, self._cmd_group)
		return self._txrFrames

	def clone(self) -> 'StreamCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StreamCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
