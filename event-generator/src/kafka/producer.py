"""Kafka producer for publishing events."""

from typing import Any
from .event_generator import generate_events_batch


def produce_events(num_events: int = 10, topic: str = "events") -> list:
    """Produce a batch of events to Kafka.
    
    Args:
        num_events: Number of events to produce.
        topic: Kafka topic to publish to.
        
    Returns:
        A list of generated events.
    """
    events = generate_events_batch(num_events)
    # In a full implementation, this would publish to Kafka
    # For now, we just return the generated events
    return events


if __name__ == "__main__":
    events = produce_events(5)
    for event in events:
        print(event)