from sqlalchemy import select

from database import SessionLocal
from models import Universe, Character


def create_universe(name: str, description: str="") -> int:
    with SessionLocal.begin() as session:
        universe = Universe(name=name, description=description or None)
        session.add(universe)
        session.flush()
        universe_id = universe.id

    return universe_id


def list_universes() -> list[dict]:
    '''
    Return a list of universe information, including universe id, name, and description.
    '''
    with SessionLocal() as session:
        universes = session.scalars(select(Universe).order_by(Universe.name)).all()
        return [
            {
                "id": universe.id,
                "name": universe.name,
                "description": universe.description
            }
            for universe in universes
        ]


def edit_universe(universe_id: int, new_name: str | None, new_desciption: str | None) -> bool:
    with SessionLocal.begin() as session:
        universe = session.get(Universe, universe_id)

        if universe is None:
            return False

        if new_name is not None:
            universe.name = new_name
        if new_desciption is not None:
            universe.description = new_desciption

    return True


def delete_universe(universe_id: int) -> bool:
    with SessionLocal.begin() as session:
        universe = session.get(Universe, universe_id)

        if universe is None:
            return False

        session.delete(universe)

    return True


def create_character(universe_id: int, name: str, description: str="") -> int | None:
    with SessionLocal.begin() as session:
        universe = session.get(Universe, universe_id)

        if universe is None:
            return None

        character = Character(name=name, description=description or None, universe=universe)
        session.add(character)
        session.flush()
        character_id = character.id

    return character_id


def edit_character(character_id: int, new_name: str | None, new_description: str | None) -> bool:
    with SessionLocal.begin() as session:
        character = session.get(Character, character_id)

        if character is None:
            return False

        if new_name is not None:
            character.name = new_name
        if new_description is not None:
            character.description = new_description
        

    return True


def delete_character(character_id: int) -> bool:
    with SessionLocal.begin() as session:
        character = session.get(Character, character_id)

        if character is None:
            return False

        session.delete(character)

    return True


def list_characters(universe_id: int) -> list[dict]:
    '''
    Return a list of character information by universe id, including character id, name, and description.
    '''
    with SessionLocal() as session:
        characters = session.scalars(select(Character).where(Character.universe_id == universe_id).order_by(Character.name)).all()
        
        # print(session.scalars(select(Character).order_by(Character.name)).all())
        return [
            {
                "id": character.id,
                "name": character.name,
                "description": character.description
            }
            for character in characters
        ]