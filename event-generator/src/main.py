"""Main entry point for the event generator application."""

from kafka.producer import produce_events


def main():
    """Main function to run the event generator."""
    print("Starting event generator...")
    events = produce_events(num_events=10, topic="user_events")
    print(f"Generated {len(events)} events")


if __name__ == "__main__":
    main()