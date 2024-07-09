"""OAuth2 for discord using the discord api."""

import requests


class DiscordAuth:
    """Discord OAuth2 class for getting user data and guild roles."""

    def __init__(self, client_id, client_secret, callback_url, guild_id):
        """Usage: credentials(client_id, client_secret, callback_url)."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.guild_id = guild_id

    def login(self):
        """
        Return a discord auth link, please manually redirect the user then it goes to the callback url with the query parameter "code" (example: https://callbackurl/?code=isfd78f2UIRFerf) to get the code to use a function called getTokens().

        The code can only be used on an active url (callback url) meaning you can only use the code once
        """
        return f"https://discord.com/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.callback_url}&scope=identify%20guilds%20guilds.members.read&response_type=code"

    def get_tokens(self, code):
        """Get the access token from the code given. The code can only be used on an active url (callback url) meaning you can only use the code once."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.callback_url,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        tokens = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        return tokens.json()

    def refresh_token(self, refresh_token):
        """Refresh access token and access tokens and will return a new set of tokens."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        tokens = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        return tokens.json()

    def get_user_data_from_token(self, access_token):
        """Get the user data from an access_token."""
        headers = {"Authorization": f"Bearer {access_token}"}

        user_data = requests.get("https://discordapp.com/api/users/@me", headers=headers)
        return user_data.json()

    def get_guild_roles(self, access_token):
        """Get the guild roles from a guild_id."""
        headers = {"Authorization": f"Bearer {access_token}"}
        roles = requests.get(f"https://discordapp.com/api/users/@me/guilds/{self.guild_id}/member", headers=headers)
        return roles.json()
