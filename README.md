# adguard-home-batch-list-manager

Add a bunch of lists to your AdGuard Home lists, including blocklists and whitelists

## Setup

1. Install [python](https://www.python.org/)
2. Install the project requirements:

    ```sh
    pip install -r requirements.txt
    ```

## Running

Run the project, and follow the prompts:

```shell
python adguard_list_manager.py
```

Alternatively, you can pass CLI args directly. For example, here is how you can clear your blacklists:

```shell
python adguard_list_manager.py --list-type blacklist --list-action clear --host YourAdGuardIPAddressHere --port YourAdGuardPortHere --username YourAdGuardUsernameHere --password YourAdGuardPasswordHere
```

And here is how you can add the ticket lists to your blacklists:

```shell
python adguard_list_manager.py --list-type blacklist --list-action add --blacklist-source firebog_ticked --host YourAdGuardIPAddressHere --port YourAdGuardPortHere --username YourAdGuardUsernameHere --password YourAdGuardPasswordHere
```

## Current Limitations

- Assumes you are not using HTTPS. It may take some refactoring to get this working with HTTPS
- Doesn't provide a way to give a custom list.

## Credits

Thanks to the user who posted on [reddit](https://pastebin.com/i1d4xNAY) and had a [pastebin](https://pastebin.com/i1d4xNAY) to get me started
