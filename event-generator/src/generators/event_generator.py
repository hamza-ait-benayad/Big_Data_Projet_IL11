import random
import uuid

from datetime import datetime, timezone, timedelta
from typing import Optional

from src.models.event import Event
from src.models.user import User


class EventGenerator:
    """Generate mobile application events using pre-generated users."""

    EVENT_TYPES = [
        "screen_view",
        "click",
        "app_open",
        "purchase",
        "scroll",
        "login",
        "signup",
    ]

    EVENT_WEIGHTS = [
        0.40,
        0.25,
        0.15,
        0.08,
        0.05,
        0.04,
        0.03,
    ]

    SCREENS = [
        "home",
        "feed",
        "details",
        "profile",
        "settings",
    ]

    def __init__(self, users, seed=None):
        """
        Initialize the generator.

        Args:
            users: List of User objects or UserPool.
            seed: Optional random seed for reproducibility.
        """

        self.users = (
            users.users if hasattr(users, "users") else users
        )

        if not self.users:
            raise ValueError(
                "You must provide generated users to create events."
            )

        for user in self.users:
            if not isinstance(user, User):
                raise ValueError("Every user must be a User instance.")

            if not user.is_valid():
                raise ValueError(
                    f"Invalid user: user_id={user.user_id!r}, "
                    f"device={user.device!r}."
                )

        self.rng = random.Random(seed)

    def _resolve_timestamp(
        self,
        custom_time: Optional[datetime] = None,
    ) -> str:
        """Return a timezone-aware UTC timestamp."""

        timestamp = custom_time or datetime.now(timezone.utc)

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)

        return timestamp.isoformat()

    def _resolve_screen(self, event_type):
        """Determine the screen associated with an event."""

        if event_type == "purchase":
            return "checkout"

        if event_type in ["screen_view", "click", "scroll"]:
            return self.rng.choice(self.SCREENS)

        return None

    def generate_event(
        self,
        user=None,
        custom_time=None,
        event_type=None,
    ) -> Event:
        """Generate a single event for a user."""

        # Select a user
        selected_user = (
            user if user is not None
            else self.rng.choice(self.users)
        )

        if selected_user not in self.users:
            raise ValueError("User does not belong to the user pool.")

        # Select event type
        if event_type is None:
            event_type = self.rng.choices(
                self.EVENT_TYPES,
                weights=self.EVENT_WEIGHTS,
                k=1,
            )[0]
        elif event_type not in self.EVENT_TYPES:
            raise ValueError(f"Invalid event type: {event_type}")

        # Determine screen
        screen = self._resolve_screen(event_type)

        # Generate timestamp
        timestamp = self._resolve_timestamp(custom_time)

        # Create event
        return Event(
            event_id=f"evt_{uuid.uuid4().hex}",
            user_id=selected_user.user_id,
            device=selected_user.device,
            event_type=event_type,
            screen=screen,
            timestamp=timestamp,
        )

    def generate_events_batch(self, size: int = 10) -> list[Event]:
        """Generate a batch of events across the user pool."""

        if size < 0:
            raise ValueError("Batch size cannot be negative.")

        return [
            self.generate_event()
            for _ in range(size)
        ]

    def generate_user_session(
        self,
        session_length: int = 5,
        user=None,
    ) -> list[Event]:
        """Generate a chronological session for one user."""

        if session_length < 1:
            raise ValueError(
                "Session length must be at least 1."
            )

        selected_user = (
            user if user is not None
            else self.rng.choice(self.users)
        )

        if selected_user not in self.users:
            raise ValueError("User does not belong to the user pool.")

        current_time = datetime.now(timezone.utc)

        events = []

        # First event: app_open
        events.append(
            self.generate_event(
                user=selected_user,
                custom_time=current_time,
                event_type="app_open",
            )
        )

        # Remaining session events
        for _ in range(session_length - 1):

            current_time += timedelta(
                seconds=self.rng.randint(2, 10)
            )

            events.append(
                self.generate_event(
                    user=selected_user,
                    custom_time=current_time,
                )
            )

        return events
