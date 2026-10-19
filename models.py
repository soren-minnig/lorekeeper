from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Universe(Base):
    __tablename__="universes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    characters: Mapped[list["Character"]] = relationship(
        back_populates="universe",
        cascade="all, delete-orphan", # Delete all children if deleted
    )


class Character(Base):
    __tablename__="characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    universe_id: Mapped[int] = mapped_column(ForeignKey("universes.id"))
    universe: Mapped["Universe"] = relationship(back_populates="characters")