from enum import Enum
from typing import Optional

import requests
import typer


class ListType(str, Enum):
    blacklist = "blacklist"
    whitelist = "whitelist"


class ListAction(str, Enum):
    add = "add"
    clear = "clear"


class BlacklistSource(str, Enum):
    firebog_ticked = "firebog_ticked"
    firebog_noncrossed = "firebog_noncrossed"
    firebog_all = "firebog_all"

    @property
    def url(self):
        # Yes, this is horrible. Typer uses the value, not the key, so this makes the user experience better"
        mappings = [
            {
                "key": BlacklistSource.firebog_ticked,
                "value": "https://v.firebog.net/hosts/lists.php?type=tick",
            },
            {
                "key": BlacklistSource.firebog_noncrossed,
                "value": "https://v.firebog.net/hosts/lists.php?type=nocross",
            },
            {
                "key": BlacklistSource.firebog_all,
                "value": "https://v.firebog.net/hosts/lists.php?type=all",
            },
        ]
        return next(item["value"] for item in mappings if item["key"] == self)


class WhitelistSource(str, Enum):
    anudeepND_safe = "anudeepND_safe"
    anudeepND_optional = "anudeepND_optional"
    anudeepND_referral = "anudeepND_referral"
    anudeepND_safe_plus_optional = "anudeepND_safe_plus_optional"

    @property
    def url(self):
        # Yes, this is horrible. Typer uses the value, not the key, so this makes the user experience better"
        mappings = [
            {
                "key": WhitelistSource.anudeepND_safe,
                "value": [
                    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt"
                ],
            },
            {
                "key": WhitelistSource.anudeepND_optional,
                "value": [
                    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt"
                ],
            },
            {
                "key": WhitelistSource.anudeepND_referral,
                "value": [
                    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/referral-sites.txt"
                ],
            },
            {
                "key": WhitelistSource.anudeepND_safe_plus_optional,
                "value": [
                    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt",
                    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt",
                ],
            },
        ]
        return next(item["value"] for item in mappings if item["key"] == self)


class AdguardListManager:
    def main(
        self,
        list_type: ListType = typer.Option(..., prompt=True),
        list_action: ListAction = typer.Option(..., prompt=True),
        blacklist_source: BlacklistSource = typer.Option(
            None, help="Use one of the predefined blacklist sources"
        ),
        whitelist_source: WhitelistSource = typer.Option(
            None, help="Use one of the predefined whitelist sources"
        ),
        custom_source_list: list[str] = typer.Option(
            None,
            help="Any custom source lists. Use this when you have one URL which just lists a bunch of URLs to add. Repeat this argument for each url. Only for blacklists",
        ),
        custom_url: list[str] = typer.Option(
            None,
            help="Any custom urls. Repeat this argument for each url. Urls will be added directly",
        ),
        host: str = typer.Option(..., prompt=True, help="Example: 192.168.1.5"),
        port: int = typer.Option(..., prompt=True, help="Example: 80"),
        username: str = typer.Option(
            ..., prompt=True, help="Username to log in to the AdGuard UI"
        ),
        password: str = typer.Option(
            ...,
            prompt=True,
            hide_input=True,
            help="Password to log into the AdGuard UI",
        ),
    ) -> None:
        self.host = f"http://{host}:{port}"
        self.get_logged_in_session(username, password)

        try:
            if list_type == ListType.blacklist and list_action == ListAction.add:
                if custom_source_list is not None and len(custom_source_list) > 0:
                    for url in list(custom_source_list):
                        self.add_blacklists_from_url(list_source_url=url)
                elif custom_url is not None and len(custom_url) > 0:
                    self.add_to_list(list(custom_url))
                elif blacklist_source is not None:
                    self.add_blacklists_from_url(list_source_url=blacklist_source.url)
                else:
                    typer.run(self.add_blacklists)
            elif list_type == ListType.blacklist and list_action == ListAction.clear:
                self.clear_list()
            elif list_type == ListType.whitelist and list_action == ListAction.add:
                if custom_url is not None and len(custom_url) > 0:
                    self.add_to_list(list(custom_url))
                if whitelist_source is not None:
                    self.add_to_list(whitelist_source.url, whitelist=True)
                else:
                    typer.run(self.add_whitelists)
            elif list_type == ListType.whitelist and list_action == ListAction.clear:
                self.clear_list(whitelist=True)
            else:
                print("Unknown or unimplemented path. Sorry!")
        except Exception as e:
            print(f"Something bad happened! See the error for more details:")
            print(e)
        finally:
            self.session.close()

    def get_logged_in_session(self, username: str, password: str) -> requests.Session:
        self.session = requests.Session()
        response = self.session.post(
            f"{self.host}/control/login", json={"name": username, "password": password}
        )
        response.raise_for_status()

    def add_blacklists_from_url(self, list_source_url: str):
        urls = self.get_lists_from_url(list_source_url)
        self.add_to_list(urls)

    def add_blacklists(
        self, list_source: BlacklistSource = typer.Option(..., prompt=True)
    ):
        urls = self.get_lists_from_url(list_source.url)
        self.add_to_list(urls)

    def add_whitelists(
        self, list_source: WhitelistSource = typer.Option(..., prompt=True)
    ):
        self.add_to_list(list_source.url, whitelist=True)

    def get_lists_from_url(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        urls = list(set(response.text.split("\n")))
        return [x for x in urls if x]

    def add_to_list(self, urls: list, whitelist: bool = False) -> None:
        for url in urls:
            response = self.session.post(
                f"{self.host}/control/filtering/add_url",
                json={"name": url, "url": url, "whitelist": whitelist},
            )
            response.raise_for_status()

    def clear_list(self, whitelist: bool = False) -> None:
        response = self.session.get(f"{self.host}/control/filtering/status")
        response.raise_for_status()

        filters = response.json().get("filters", [])
        if filters is not None:
            for filter in filters:
                response = self.session.post(
                    f"{self.host}/control/filtering/remove_url",
                    json={"url": filter["url"], "whitelist": whitelist},
                )
                response.raise_for_status()


if __name__ == "__main__":
    instance = AdguardListManager()
    typer.run(instance.main)
