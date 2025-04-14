from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import final

from sqlalchemy import Insert, insert
from sqlalchemy.orm import DeclarativeBase

from .dto import HistoryCreateDTO


class BaseInsertStmtBuilder(ABC):  # pragma: no cover
    def __init__(self, history_model: type[DeclarativeBase]) -> None:
        self._history_model = history_model

    @abstractmethod
    def build(
        self,
        dtos: Sequence[HistoryCreateDTO],
    ) -> Insert:
        pass


@final
class InsertStmtBuilder(BaseInsertStmtBuilder):
    def build(
        self,
        dtos: Sequence[HistoryCreateDTO],
    ) -> Insert:
        return insert(self._history_model).values([dto.to_dict() for dto in dtos])
