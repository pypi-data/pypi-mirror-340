import inspect

from .domain import Auto
from .service_layer import handlers, UnitOfWork, MessageBus
from .domain.models import Environment


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {name: dependency for name, dependency in dependencies.items() if name in params}
    return lambda message: handler(message, **deps)


def bootstrap(uow: UnitOfWork = Auto, env: Environment = Auto) -> MessageBus:
    """Creates a new MessageBus instance with all dependencies injected."""
    if not uow:
        uow = UnitOfWork()
    if not env:
        env = Environment()

    dependencies = {"uow": uow, "env": env}
    injected_event_handlers = {
        event_type: [inject_dependencies(handler, dependencies) for handler in event_handlers]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return MessageBus(
        uow=uow, env=env, event_handlers=injected_event_handlers, command_handlers=injected_command_handlers
    )
