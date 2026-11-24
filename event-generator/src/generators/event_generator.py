"""Event generator module for producing synthetic events."""

import json
import random
import time
from datetime import datetime, timezone
from typing import Dict, Any


def generate_event(event_type: str = None) -> Dict[str, Any]:
    """Generate a synthetic event with the given type.
    
    Args:
        event_type: Type of event to generate. If None, a random type is chosen.
        
    Returns:
        A dictionary representing the generated event.
    """
    types = ["click", "view", "purchase", "signup", "login"]
    if event_type is None:
        event_type = random.choice(types)
    
    event = {
        "event_id": f"evt_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "properties": {
            "user_id": f"user_{random.randint(1000, 9999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
        }
    }
    
    # Type-specific properties
    if event_type == "click":
        event["properties"]["page_url"] = f"https://example.com/page{random.randint(1, 10)}"
        event["properties"]["element"] = random.choice(["button", "link", "banner"])
    elif event_type == "view":
        event["properties"]["page_url"] = f"https://example.com/page{random.randint(1, 10)}"
        event["properties"]["duration"] = random.randint(1, 30)
    elif event_type == "purchase":
        event["properties"]["product_id"] = f"prod_{random.randint(100, 999)}"
        event["properties"]["amount"] = round(random.uniform(10.0, 500.0), 2)
        event["properties"]["currency"] = "USD"
    elif event_type == "signup":
        event["properties"]["method"] = random.choice(["email", "google", "github"])
    elif event_type == "login":
        event["properties"]["method"] = random.choice(["email", "google", "password"])
    
    return event


def generate_events_batch(size: int = 10, event_type: str = None) -> list:
    """Generate a batch of synthetic events.
    
    Args:
        size: Number of events to generate.
        event_type: Type of events to generate. If None, random types are used.
        
    Returns:
        A list of event dictionaries.
    """
    return [generate_event(event_type) for _ in range(size)]


if __name__ == "__main__":
    # Simple test when run directly
    event = generate_event()
    print(json.dumps(event, indent=2))