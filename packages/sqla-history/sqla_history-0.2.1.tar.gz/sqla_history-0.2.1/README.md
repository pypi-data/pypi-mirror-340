# SQLAlchemy History

SQLAlchemy History is an extension for SQLAlchemy that provides change tracking and history logging for SQLAlchemy models. It allows developers to easily track changes to their database objects over time, providing a comprehensive history of modifications.

## Features

- Track changes made to SQLAlchemy models.
- Log historical data for audit purposes.
- Easily integrate with existing SQLAlchemy applications.

## How it works

When you change model fields and add the model to a session, via `session.add(model)` or `session.add_all([model])`, the event listener `"after_update"` you defined is triggered. This listener monitors for changes to field values. If changes have been made, an object containing the field changes (`HistoryChanges`) will be added to the corresponding table.

## Installation

To install SQLAlchemy History, call this command:

```bash
pip install sqla-history
```

or

```bash
uv add sqla-history
```

## Usage

### Implementation HistoryModel

First, determine the model.
You should define the field `entity_id`.
You can also define an FK field with a User ID if you need to track who exactly made changes to the model.

Example:

```python
from sqla_history import BaseHistoryChanges


class Base(DeclarativeBase):
    metadata = meta


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    ...

...


class HistoryChanges(BaseHistoryChanges, Base):
    __tablename__ = "history_changes"

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    entity_id: Mapped[UUID] = mapped_column(index=True)
```

### Creation event listener

In this step you need to create an event listener with `"after_update"` type.

Example:

```python
from sqlalchemy import Connection, String, event
from sqlalchemy.orm import Mapped, Mapper
from sqla_history import InsertStmtBuilder, WithUserChangeEventHandler

class Note(Base):
    __tablename__ = "note"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


@event.listens_for(Note, "after_update")
def create_note_history(
    mapper: Mapper,
    connection: Connection,
    target: Note,
) -> None:
    stmt_builder = InsertStmtBuilder(history_model=HistoryChanges)
    handler = WithUserChangeEventHandler(
        entity_name="note",
        stmt_builder=stmt_builder,
    )
    handler(mapper=mapper, connection=connection, target=target)
```

[See full example](https://gitlab.com/n.one.k/opensource/sqla-history/-/tree/main/examples)

### Important notes

- define event listeners in the **same module as the model**
- don't forget to define the **`entity_id`** field

Tested SQLAlchemy Events:

- "after_update"
