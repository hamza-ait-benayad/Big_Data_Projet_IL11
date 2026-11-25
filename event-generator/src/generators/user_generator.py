import random
from typing import Optional

from src.models.user import User


class UserGenerator:
    """Generate a pool of users for mobile application analytics."""

    DEFAULT_DEVICE_DISTRIBUTION = {
        "Android": 0.6,
        "iOS": 0.4,
    }

    VALID_DEVICES = ["Android", "iOS"]

    def __init__(
        self,
        num_users: int = 100,
        device_distribution: Optional[dict] = None,
        seed: Optional[int] = None,
    ):
        if num_users < 1:
            raise ValueError("num_users must be at least 1.")

        self.num_users = num_users

        self.rng = random.Random(seed)

        self.device_distribution = (
            device_distribution.copy()
            if device_distribution is not None
            else self.DEFAULT_DEVICE_DISTRIBUTION.copy()
        )

        self._validate_distribution()

        self.users: list[User] = []

    def _validate_distribution(self):
        """Validate device probabilities."""

        if not self.device_distribution:
            raise ValueError("Device distribution cannot be empty.")

        for device, weight in self.device_distribution.items():

            if device not in self.VALID_DEVICES:
                raise ValueError(f"Invalid device: {device}")

            if not isinstance(weight, (int, float)):
                raise ValueError("Device weights must be numeric.")

            if weight < 0:
                raise ValueError("Device weights cannot be negative.")

        if sum(self.device_distribution.values()) <= 0:
            raise ValueError("At least one device weight must be positive.")

    def generate_users(self) -> list[User]:

        self.users = []

        devices = list(self.device_distribution.keys())
        weights = list(self.device_distribution.values())

        for _ in range(self.num_users):
            device = self.rng.choices(
                devices,
                weights=weights,
                k=1,
            )[0]

            user = User(device=device)
            self.users.append(user)
        return self.users

    def get_user_ids(self) -> list[str]:
        return [user.user_id for user in self.users]

    def get_user(self, user_id: str) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None


class UserPool:
    def __init__(self, users: Optional[list[User]] = None):

        self.users = list(users) if users is not None else []

        self.user_map = {
            user.user_id: user
            for user in self.users
        }

        if len(self.user_map) != len(self.users):
            raise ValueError("Duplicate user IDs found.")

    def get_random_user(self) -> User:
        if not self.users:
            raise ValueError("UserPool is empty.")
        return random.choice(self.users)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_map.get(user_id)

    def get_user_id(self) -> str:
        return self.get_random_user().user_id

    def __len__(self):
        return len(self.users)
