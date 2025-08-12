from app.api.shared.aggregate.aggregate_root import AggregateRoot


class User(AggregateRoot):
    """
    Represents a user in the system.
    Inherits from AggregateRoot to ensure it has a unique identifier.

    :since: 0.0.1
    """

    __slots__ = AggregateRoot.__slots__ + ("username", "email")

    def __init__(self, _id: str, username: str, email: str) -> None:
        """
        Initializes a new User with the specified id, username, and email.

        :param _id: Unique identifier of the User.
        :param username: Username of the User.
        :param email: Email address of the User.
        """
        super().__init__(_id)
        self.username = username
        self.email = email

    def __repr__(self) -> str:
        return f"<User id={self._id}, username={self.username}, email={self.email}>"

    def to_dict(self) -> dict[str, str]:
        """
        Converts the User instance to a dictionary representation.

        :return: Dictionary containing the User's id, username, and email.
        """
        return {
            "id": self._id,
            "username": self.username,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "User":
        """
        Creates a User instance from a dictionary representation.

        :param data: Dictionary containing the User's id, username, and email.
        :return: User instance created from the provided dictionary.
        """
        return cls(
            _id=data["id"],
            username=data["username"],
            email=data["email"],
        )
