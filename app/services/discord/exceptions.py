class DiscordAPIError(Exception):
    pass


class UncorrectDiscordTag(DiscordAPIError):
    pass


class CantAddFriend(DiscordAPIError):
    pass


class CantRemoveFriend(DiscordAPIError):
    pass


class AlreadyFriend(DiscordAPIError):
    pass


class FriendRequestDisabled(DiscordAPIError):
    pass


class DiscordTagNotFound(DiscordAPIError):
    pass


class FriendNotFound(DiscordAPIError):
    pass


class Unauthorized(DiscordAPIError):
    pass
