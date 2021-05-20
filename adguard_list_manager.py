from enum import Enum

import requests
import typer


class ListType(str, Enum):
    blacklist = "blacklist"
    whitelist = "whitelist"


class ListAction(str, Enum):
    add = "add"
    clear = "clear"


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
    ):
        self.host = f"http://{host}:{port}"
        self.get_logged_in_session(username, password)

        try:
            if list_type == ListType.blacklist and list_action == ListAction.add:
                self.add_to_blacklist()
            else:
                print("Unknown or unimplemented path. Sorry!")
        except Exception as e:
            print(f"Something bad happened! See the error for more details: {e}")
        finally:
            self.session.close()

    def get_logged_in_session(self, username: str, password: str) -> requests.Session:
        self.session = requests.Session()
        logged_in_session = self.session.post(
            f"{self.host}/control/login", json={"name": username, "password": password}
        )
        logged_in_session.raise_for_status()

    def add_to_blacklist(self):
        urls = [
            "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt",
            "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts",
            "https://v.firebog.net/hosts/static/w3kbl.txt",
            "https://adaway.org/hosts.txt",
            "https://v.firebog.net/hosts/AdguardDNS.txt",
            "https://v.firebog.net/hosts/Admiral.txt",
            "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
            "https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt",
            "https://v.firebog.net/hosts/Easylist.txt",
            "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",
            "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts",
            "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts",
            "https://v.firebog.net/hosts/Easyprivacy.txt",
            "https://v.firebog.net/hosts/Prigent-Ads.txt",
            "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts",
            "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt",
            "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt",
            "https://raw.githubusercontent.com/Kees1958/W3C_annual_most_used_survey_blocklist/master/TOP_EU_US_Ads_Trackers_HOST",
            "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareHosts.txt",
            "https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt",
            "https://s3.amazonaws.com/lists.disconnect.me/simple_malvertising.txt",
            "https://v.firebog.net/hosts/Prigent-Crypto.txt",
            "https://bitbucket.org/ethanr/dns-blacklists/raw/8575c9f96e5b4a1308f2f12394abd86d0927a4a0/bad_lists/Mandiant_APT1_Report_Appendix_D.txt",
            "https://phishing.army/download/phishing_army_blocklist_extended.txt",
            "https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-malware.txt",
            "https://v.firebog.net/hosts/Shalla-mal.txt",
            "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt",
            "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts",
            "https://urlhaus.abuse.ch/downloads/hostfile/",
            "https://zerodot1.gitlab.io/CoinBlockerLists/hosts_browser",
        ]

        for url in urls:
            add = self.session.post(
                f"{self.host}/control/filtering/add_url",
                json={"name": url, "url": url, "whitelist": False},
            )
            add.raise_for_status()

    def clear_blacklist():
        pass


if __name__ == "__main__":
    instance = AdguardListManager()
    typer.run(instance.main)
