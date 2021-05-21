from enum import Enum

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


class AdguardListManager:
    def main(
        self,
        list_type: ListType = typer.Option(..., prompt=True),
        list_action: ListAction = typer.Option(..., prompt=True),
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
                typer.run(self.add_blacklists)
            elif list_type == ListType.blacklist and list_action == ListAction.clear:
                self.clear_list()
            elif list_type == ListType.whitelist and list_action == ListAction.add:
                self.add_to_list(whitelist=True)
            elif list_type == ListType.whitelist and list_action == ListAction.clear:
                self.clear_list(whitelist=True)
            else:
                print("Unknown or unimplemented path. Sorry!")
        except Exception as e:
            print(f"Something bad happened! See the error for more details: {e}")
        finally:
            self.session.close()

    def get_logged_in_session(self, username: str, password: str) -> requests.Session:
        self.session = requests.Session()
        response = self.session.post(
            f"{self.host}/control/login", json={"name": username, "password": password}
        )
        response.raise_for_status()

    def add_blacklists(
        self, list_source: BlacklistSource = typer.Option(..., prompt=True)
    ):
        urls = self.get_lists_from_url(list_source.url)
        self.add_to_list(urls)

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
        for filter in filters:
            response = self.session.post(
                f"{self.host}/control/filtering/remove_url",
                json={"url": filter["url"], "whitelist": whitelist},
            )
            response.raise_for_status()


if __name__ == "__main__":
    instance = AdguardListManager()
    typer.run(instance.main)
