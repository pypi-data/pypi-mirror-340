from collections import defaultdict
from typing import Generic, DefaultDict, Callable, Type

from kevent.event import EVENT_T


class EventDispatcher(Generic[EVENT_T]):
    def __init__(self):
        # tipo de evento -> lista de callbacks
        self._listeners: DefaultDict[Type[EVENT_T], list[Callable[[EVENT_T], None]]] = defaultdict(list)

    def has_subscribers(self, event_type: Type[EVENT_T]) -> bool:
        """Verifica si hay suscriptores exactamente para el tipo dado."""
        return event_type in self._listeners and len(self._listeners[event_type]) > 0

    def subscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        """Registra un callback para un tipo de evento."""
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        """Elimina un callback registrado para un tipo de evento."""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    def dispatch(self, event: EVENT_T):
        """Lanza el evento a los callbacks registrados para su tipo exacto."""
        event_type = type(event)
        for callback in self._listeners.get(event_type, []):
            callback(event)

    def __repr__(self):
        listeners_repr = ",\n".join(
            f"  {event_type.__name__}: {len(callbacks)} subscriber(s)"
            for event_type, callbacks in self._listeners.items()
        )
        return f"EventDispatcher(\n{listeners_repr}\n)"
