"""Callbacks which integrate with and/or modify the behavior of model optimizers."""
from __future__ import annotations

import datetime
import math
import typing
from typing import Any, Callable, Mapping, MutableMapping, Optional, Type

from overrides import overrides
import torch
from torch.optim.lr_scheduler import _LRScheduler, ReduceLROnPlateau
from typing_extensions import Literal

from forecast.callbacks.callback import Callback
from forecast.callbacks.utils import CallbackDistributedExecMode
from forecast.utils import EarlyTerminationException

if typing.TYPE_CHECKING:
    from forecast.distributed import Communicator


class LRScheduleCallback(Callback):
    """Wraps a generic learning rate schedule in a callback."""

    def __init__(self, scheduler_type: Type[_LRScheduler], **schedular_kwargs: Any):
        """Wraps a generic learning rate schedule in a callback.

        Parameters
        ----------
        scheduler_type: Type[_LRScheduler]
            A learning rate scheduler type which only requires the current epoch to step
        schedular_kwargs: dict
            kwargs to pass to the learning rate scheduler upon creation

        """
        super().__init__()
        self._sched: Optional[_LRScheduler] = None
        self._sched_type = scheduler_type
        self._sched_kwargs = schedular_kwargs

    @overrides
    def on_train_val_epoch_end(self, epoch: int) -> None:
        """Steps the learning rate scheduler.

        Parameters
        ----------
        epoch: int
            The current epoch

        Returns
        -------
        None

        """
        if not self._sched:
            self._sched = self._sched_type(**self._sched_kwargs)
        self._sched.step(epoch)

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


class ReduceLROnPlateauCallback(Callback):
    """Wraps a ReduceLROnPlateau schedule in a callback."""

    def __init__(self, metric_name: str, **scheduler_kwargs: Any):
        """Wraps a ReduceLROnPlateau schedule in a callback.

        Parameters
        ----------
        metric_name: str
            The name of the metric to be examined for plateau (or 'loss' if the loss function should be monitored)
        scheduler_kwargs: dict
            kwargs passed to the ReduceLROnPlateau scheduler

        """
        super().__init__()
        self._sched: Optional[ReduceLROnPlateau] = None
        self._sched_kwargs = scheduler_kwargs
        self._metric_name = metric_name

    @overrides
    def on_val_end(self, epoch: int, loss: float, metrics: Mapping[str, float]) -> None:
        """Examines whether the specified metric has plateaued.

        Parameters
        ----------
        epoch: int
            The current epoch
        loss: float
            The current value of the loss
        metrics: Mapping[str, float]
            The model's performance on the validation set during the current epoch

        Returns
        -------
        None

        """
        if self._metric_name == "loss":
            m = loss
        else:
            m = metrics[self._metric_name]
        if not self._sched:
            self._sched = ReduceLROnPlateau(self.optimizer, **self._sched_kwargs)
        self._sched.step(m, epoch)

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


class EarlyStoppingCallback(Callback):
    """Terminates training early if the specified metric continually fails to improve."""

    def __init__(
        self,
        patience: int,
        min_improvement: float,
        metric: Optional[str] = None,
        mode: Literal["min", "max"] = "min",
        improvement_type: Literal["relative", "absolute"] = "relative",
        callback: Optional[Callable[[int, float, float], None]] = None,
    ):
        """Prematurely ends the training regimen in the val loss doesn't improve for a fixed number of epochs.

        Parameters
        ----------
        patience: int
            The number of epochs to wait for improvement before forcing termiantion
        min_improvement: float
            The size of the improvement required to be marked as a "realized" improvement
        metric: Optional[str]
            If None, uses the val loss to assess improvement. Otherwise, uses the specified metric. Defaults to None.
        mode: Literal["min", "max"]
            Whether the target value should decrease or increase in value. Defaults to min.
        improvement_type: Literal["relative", "absolute"]
            Whether the min_improvement specifies an absolute improvement value or a percent improvement. Defaults to
            relative.
        callback: Optional[Callback[[int, float, float], None]]
            A callback to be invoked upon the last computation of the validation metric prior to early termination. Is
            passed the epoch, current metric value, and best metric value. If None is supplied, no callback is invoked.
            Defaults to None.
        """
        super().__init__()

        if patience < 0:
            raise ValueError("Parameter `patience` must be >= 0.")
        if min_improvement < 0:
            raise ValueError("Parameter `min_improvement` must be >= 0.")

        self.patience = patience
        self.steps_since_improvement = 0
        self.metric = metric
        self._callback = callback
        self._terminate = False

        mode = mode.lower()
        if mode not in ("min", "max"):
            raise ValueError('Parameter `mode` must be one of ("min", "max").')
        self.mode = mode
        self.best_score = float("inf") if self.mode == "min" else float("-inf")
        if self.mode == "min":
            min_improvement *= -1

        improvement_type = improvement_type.lower()
        if improvement_type not in ("relative", "absolute"):
            raise ValueError('Parameter `improvement_type` must be one of ("relative", "absolute").')
        self.improvement_type = improvement_type
        if self.improvement_type == "relative":
            min_improvement += 1

        self.min_improvement = min_improvement

    def _get_thresh(self) -> float:
        if self.improvement_type == "relative":
            return self.best_score * self.min_improvement
        else:
            return self.best_score + self.min_improvement

    @overrides
    def on_val_end(self, epoch: int, loss: float, metrics: Mapping[str, float]) -> None:
        """Determines whether the validation metric has improved.

        Parameters
        ----------
        epoch: int
            The current epoch
        loss: float
            The current validation loss
        metrics: Mapping[str, float]
            A set of user-defined metrics evaluated every pass through the validation set

        Returns
        -------
        None

        """
        score = loss if self.metric is None else metrics[self.metric]
        thresh = self._get_thresh()
        improved = score < thresh if self.mode == "min" else score > thresh

        if improved:
            self.steps_since_improvement = 0
            self.best_score = score
        else:
            self.steps_since_improvement += 1

        if self.steps_since_improvement >= self.patience:
            if self._callback:
                self._callback(epoch, score, self.best_score)
            self._terminate = True

    @overrides
    def on_train_val_epoch_end(self, epoch: int) -> None:
        """Terminates training if appropriate by raising an EarlyTerminationException."""
        _maybe_terminate(self._terminate, self.communicator)

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


class MaxTrainingTimeCallback(Callback):
    """Terminates training after a pre-specified amount of time."""

    def __init__(self, max_time: float):
        """The max amount of time, in seconds, for which training can run."""
        super().__init__()
        self._max_time = datetime.timedelta(seconds=max_time)
        self._start: Optional[datetime.datetime] = None

    @overrides
    def on_train_begin(self) -> None:
        """Stores the start time when training begins."""
        self._start = datetime.datetime.now()

    @overrides
    def on_train_val_epoch_end(self, epoch: int) -> None:
        """Terminates training if our time budget has been consumed."""
        assert self._start is not None
        _maybe_terminate(datetime.datetime.now() - self._start > self._max_time, self.communicator)

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


class PreemptTimeLimitCallback(Callback):
    """Terminates training prior to reaching a predeterminted time limit."""

    def __init__(self, end_time: datetime.datetime, margin: float = 0.1):
        """Creates a callback which terminates if the next epoch may potentially timeout.

        Parameters
        ----------
        end_time: datetime
            The time at which the experiment will timeout
        margin: float, optional
            How much buffer to permit, defaults to 0.1. A margin of X implies the experiment will terminate if
            (1+X) * last_epoch_time will exceed the time remaining.
        """
        super().__init__()
        self._tz = end_time.tzinfo  # capture timezone from supplied end time and use it when fetching time elsewhere
        now = datetime.datetime.now(self._tz)
        if end_time < now:
            raise ValueError(f"`end_time` cannot be in the past; received {end_time} but it's currently {now}")
        if margin < 0:
            raise ValueError(f"`margin` must be >= 0; received {margin}")

        self._end_time = end_time
        self._margin = margin
        self._epoch_start_time: Optional[datetime.datetime] = None

    @overrides
    def on_train_epoch_begin(self, epoch: int) -> None:
        """Updates the epoch start time."""
        self._epoch_start_time = datetime.datetime.now(self._tz)

    @overrides
    def on_train_val_epoch_end(self, epoch: int) -> None:
        """Determines whether the training should be terminated at the end of the epoch."""
        assert self._epoch_start_time is not None
        now = datetime.datetime.now(self._tz)
        _maybe_terminate(
            (now - self._epoch_start_time) * (1 + self._margin) + now > self._end_time,
            self.communicator,
        )
        self._epoch_start_time = now

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


class NotFiniteTrainingLossCallback(Callback):
    """Terminates training if N consecutive training batches have a NaN/Inf/-Inf loss."""

    def __init__(self, num_non_finite: int, raise_on_epoch: bool = False):
        """Terminates training if num_non_finite consecutive training batches have a NaN/Inf/-Inf loss.

        Parameters
        ----------
        num_non_finite: int
            The number of non-finite batch losses to allow before termination.
        raise_on_epoch: bool, optional
            If true, only raises on epoch end rather than batch end. Defaults to False.
        """
        super().__init__()
        if num_non_finite < 0:
            raise ValueError(f"`num_nans` must be > 0; received {num_non_finite}")
        self._max_bad = num_non_finite
        self._cur_bad = 0
        self._raise_on_epoch = raise_on_epoch

    @overrides
    def on_train_batch_end(self, epoch: int, batch: int, loss: float) -> None:
        """Determines at the end of every batch whether to terminate training.

        Parameters
        ----------
        epoch: int
            The training epoch
        batch: int
            The batch index
        loss: float
            The batch loss

        Returns
        -------
        None
        """
        is_finite = math.isfinite(loss)
        if is_finite:
            self._cur_bad = 0
        else:
            self._cur_bad += 1
        if not self._raise_on_epoch:
            _maybe_terminate(self._cur_bad >= self._max_bad, self.communicator)

    @overrides
    def on_train_epoch_end(self, epoch: int, loss: float, metrics: MutableMapping[str, float]) -> None:
        if self._raise_on_epoch:
            _maybe_terminate(self._cur_bad >= self._max_bad, self.communicator)

    @staticmethod
    @overrides
    def get_distributed_exec_mode() -> CallbackDistributedExecMode:
        return CallbackDistributedExecMode.ALL


def _maybe_terminate(b: bool, comm: Communicator) -> None:
    t = torch.tensor([b], dtype=torch.float32)
    with torch.no_grad():
        terminate = comm.allreduce(t)
    if terminate > 0:
        raise EarlyTerminationException
