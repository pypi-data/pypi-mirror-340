from logging import getLogger

from sqlalchemy import Connection, inspect
from sqlalchemy.orm import DeclarativeBase, Mapper

from sqla_history.stmt_builder import InsertStmtBuilder

from .context import CurrentUserId, EventId
from .dto import HistoryCreateDTO, Value
from .not_set import NOT_SET, NotSet
from .types_ import UserId
from .utils import utc_now

logger = getLogger(__name__)


class ChangeEventHandler:
    def __init__(
        self,
        entity_name: str,
        stmt_builder: InsertStmtBuilder,
        id_field_name: str = "id",
    ) -> None:
        self._entity_name = entity_name
        self._stmt_builder = stmt_builder
        self._id_field_name = id_field_name

    def __call__(
        self,
        mapper: Mapper,
        connection: Connection,
        target: DeclarativeBase,
    ) -> None:
        if (event_id := EventId.get()) is None:
            logger.info("event_id is None. Changes wasn't tracked")
            return

        state = inspect(target)
        ident = getattr(target, self._id_field_name)
        changed_at = utc_now()

        dtos: list[HistoryCreateDTO] = []
        for attr in mapper.columns:
            field_name = attr.key
            new_value = getattr(target, field_name)
            attribute_state = state.attrs[field_name]
            if not attribute_state.history.deleted:
                continue

            prev_value = attribute_state.history.deleted[0]
            if prev_value == new_value:  # pragma: no cover
                # no cover as the case could not be reproduced
                continue

            dtos.append(
                HistoryCreateDTO(
                    event_id=event_id,
                    entity_id=ident,
                    entity_name=self._entity_name,
                    changed_at=changed_at,
                    field_name=field_name,
                    prev_value=Value(prev_value).model_dump(mode="json"),
                    new_value=Value(new_value).model_dump(mode="json"),
                    user_id=self._get_user_id(),
                )
            )

        if not dtos:
            return

        stmt = self._stmt_builder.build(dtos)
        connection.execute(stmt)

    def _get_user_id(self) -> UserId | None | NotSet:
        return NOT_SET


class WithUserChangeEventHandler(ChangeEventHandler):
    def _get_user_id(self) -> UserId | None | NotSet:
        return CurrentUserId.get()
