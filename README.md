# adguard-home-batch-list-manager

Allows you to manage your AdGuard Home lists, including blocklists and whitelists

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
python adguard_list_manager.py \
    --host YourAdGuardIPAddressHere \
    --port YourAdGuardPortHere \
    --username YourAdGuardUsernameHere \
    --password YourAdGuardPasswordHere \
    --list-type blacklist \
    --list-action clear
```

And here is how you can add the ticket lists to your blacklists:

```shell
python adguard_list_manager.py \
    --host YourAdGuardIPAddressHere \
    --port YourAdGuardPortHere \
    --username YourAdGuardUsernameHere \
    --password YourAdGuardPasswordHere \
    --list-type blacklist \
    --list-action add \
    --blacklist-source firebog_ticked
```

### Using Custom URL's

The CLI args do support custom URL's if you don't like the sources.

The order in which the arguments are used are:

1. `custom-source-list` via CLI
2. `custom-url` via CLI
3. `blacklist-source` via CLI
4. `blacklist-source` via prompt

The same pattern is repeated for whitelist, though `custom-source-list` doesn't apply to whitelist.

If you have a URL which defines multiple URL's to add (like firebog), use the `custom-source-list` argument. You can repeat this if needed:

```shell
python adguard_list_manager.py \
    --host YourAdGuardIPAddressHere \
    --port YourAdGuardPortHere \
    --username YourAdGuardUsernameHere \
    --password YourAdGuardPasswordHere \
    --list-type blacklist \
    --list-action add \
    --custom-source-list http://TheFirstURL.com \
    --custom-source-list http://TheSecondURL.com
```

Alternatively, if you just have a bunch of URL sources with rules in them, you can add them using the `custom-url` argument, repeated for each url if needed:

```shell
python adguard_list_manager.py \
    --host YourAdGuardIPAddressHere \
    --port YourAdGuardPortHere \
    --username YourAdGuardUsernameHere \
    --password YourAdGuardPasswordHere \
    --list-type blacklist \
    --list-action add \
    --custom-url http://TheFirstURL.com \
    --custom-url http://TheSecondURL.com
```

## Current Limitations & Things To Improve

- Assumes you are not using HTTPS. It may take some refactoring to get this working with HTTPS
- No unit tests for now

## Credits

Thanks to the user who posted on [reddit](https://pastebin.com/i1d4xNAY) and had a [pastebin](https://pastebin.com/i1d4xNAY) to get me started
