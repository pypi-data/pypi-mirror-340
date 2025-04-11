from seatsurfing.booking import Bookings


class Client:
    """Client to interact with Seatsurfing."""

    def __init__(
        self, base_url: str, organization_id: str, username: str, password: str
    ):
        self.booking = Bookings(
            base_url=base_url,
            organization_id=organization_id,
            username=username,
            password=password,
        )
