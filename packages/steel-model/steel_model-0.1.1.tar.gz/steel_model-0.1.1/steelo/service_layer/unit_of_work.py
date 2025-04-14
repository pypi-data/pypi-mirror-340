from typing import Self

from ..adapters.repositories import Repository
from ..adapters.repositories.in_memory_repository import InMemoryRepository
from ..domain import Auto


class UnitOfWork:
    repository: Repository

    def __init__(self, repository: Repository = Auto) -> None:
        if not repository:
            repository = InMemoryRepository()
        self.repository = repository
        self.plants = repository.plants
        self.furnace_groups = repository.furnace_groups
        self.demand_centers = repository.demand_centers

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        pass

    def rollback(self):
        pass

    def collect_new_events(self):
        for plant in self.plants.seen:
            while plant.events:
                yield plant.events.pop(0)
