[![Discord](https://img.shields.io/discord/675390855716274216.svg)](https://discord.gg/5yXExTsRye)

# DCustomRPC: The Rewrite!

**The icon used for this project is [here](https://www.shareicon.net/logo-website-discord-887435).**

DCustomRPC is a custom rich presence client that you (you right there, yes you) can customize.

![intro_img](https://i.imgur.com/8Pf5HjT.png)

## Setting up the config:
The config should be fairly easy to setup:
1. Firstly go to Discord Developers (https://discord.com/developers/applications/) and sign in.
2. From here, click the "New App" button and enter a "App Name". This will show as what you are playing. "App Description" and "App Icon" do not matter for rich presence.
3. After you have done this, you can copy the "Client ID" (under "App Details") and replace the client_id already in the config file.
4. To setup the game list, we will need to separate each of the games by a "-" with the spacing from the config for the dashes and the remaining keys. Each game can contain the following:
    - `details` - This is the shorter description for the game:

        ![details](https://i.imgur.com/9Z7OdfI.png)
    - `state` - This is the longer description for the game:

        ![state](https://i.imgur.com/i1YbCfd.png)
    - `large_image` - The image key for the large image on the game. In order to attach your image to a key, open up your Discord Developers page for your app and scroll down to "Rich Presence Assets". From here, since we want a large image, we upload the image, enter the key (which we will write in the config) and select "Large". Then make sure to click "Upload Asset" and "Save Changes". After we add to the config, this will look like this:

        ![lg_image](https://i.imgur.com/KbQdc61.png)
    - `large_text` - This will be the text for when you hover over the large image:

        ![lg_text](https://i.imgur.com/nNRHtxo.png)
    - `small_image` - The image key for the small image on the game. In order to attach your image to a key, open up your Discord Developers page for your app and scroll down to "Rich Presence Assets". From here, since we want a small image, we upload the image, enter the key (which we will write in the config) and select "Small". Then make sure to click "Upload Asset" and "Save Changes". After we add to the config, this will look like this:

        ![sm_image](https://i.imgur.com/wjo0Nkx.png)
    - `small_text` - This will be the text for when you hover over the small image:

        ![sm_text](https://i.imgur.com/EApOnTl.png)
    - `buttons` - A list of dicts containing buttons and their URLs. Up to two buttons can be specified.
   
        ![buttons](https://cdn.discordapp.com/attachments/796094479903096902/820843690796515368/unknown.png)

## Useful Links
[Python 3.6.6](https://www.python.org/downloads/release/python-366/) 

[Repo Download: Stable](https://github.com/tazz4843/DCustomRPC/archive/master.zip) 

[Support Server](https://discord.gg/5yXExTsRye)

## Discord prerequisites:
Please make sure that game statuses are turned on:

![Game Toggle](https://i.imgur.com/V4FWevH.png)

## Setting up DCustomRPC:
DCustomRPC requires Python 3.6+. If you have anything older installed, you will need to install Python 3.6+ and make sure it is added to the PATH. From here, you can run `py -m pip install -r requirements.txt` (the `py` bit might change to `python3.5`/`python3.6`, try that if you can't get that to work).

## Starting DCustomRPC in the commandline:

In order to check everything is working in the command line, you can run `py dcustomrpc.pyw`.

## Starting DCustomRPC on boot
### Linux (untested, but should work)

Add `python3 /path/to/dcustomrpc.pyw &` to `/etc/rc.local`. Don't forget the `&` at the end of the line otherwise your system will not boot!
### Windows

I don't run Winshit, so I can't check this. If anyone has info, please make a PR!
"# Discord-Rich-prescence" 
