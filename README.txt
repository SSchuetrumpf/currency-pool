How to configure Currency Pool

1. Open Streamlabs Chatbot
2. Navigate to Scripts
3. Click on Import Scripts icon
4. Select CurrencyPool.zip.
5. After scripts as refreshed, right click on the script and select "Insert API Key", then click "Yes"
6. Log into Streamlabs Dashboard.
7. Navigate to API Settings -> API Tokens
8. Copy "Your API Access Token"
9. Paste API token into "Overlay" section of Currency Pool script settings

Using the Overlay

1. Open stream application, presumably OBS.
2. Add a new browser Source
3. Select Local File, then Browse
4. Navigate to the Currency Pool overlay directory
    i. By default, this is C:\Users\<your user>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts\CurrencyPool\Overlay
5. Open "index.html"


It is recommended to leave "Shutdown source when not visible" and "Refresh browser when scene becomes active" unchecked.

If the overlay comes up and displays the text "Connected to bot.", then everything is working properly.
Simply navigate to Scripts -> Currency Pool -> Overlay and select "Refresh Overlay" to update the overlay


Upgrade Instructions:
1. Backup config.js, config.json, and currencypool_lib/model/persistence/storage.json
2. Delete CurrencyPool directory
3. Reimport CurrencyPool.zip
4. Replace config.js, config.json, and storage.json with backed up versions
    i. When upgrading from 1.0.0 to 1.1.0, storage.json now goes in the same folder as config.js and config.json.
5. Regenerate API key. (Right click script -> Insert API Key)


Changelog:
    1.1.0:
        * Removed "Enabled" checkbox from core configuration. It duplicated functionality provided by the script level "Enabled" checkbox
        * Fixed !pool top showing contributors with 0 contributions. This happened if someone contributed then refunded their points.
        * Fixed label for commit confirmation message
        * Moved storage.json to script root
        * Fixed OverlayApi throwing an error if no streamlabs api token is provided. Should now use default settings if no api token
        * Added style selector for choosing overlay style between donation goal, follower goal, bit goal, and sub goal.

Things to Note:
1. Streamlabs Chatbot should be open BEFORE opening OBS or adding the overlay. If Chatbot is not open first, an error message will
be displayed in the overlay and you will have to refresh the browser source.

2. If there is no goal and target currently set, the overlay will be hidden.


Available commands:

!pool
    Displays the current goal information including remaining currency.

!pool add <number>
    Donates <number> points to the pool. The viewer must have the points available or an error will be displayed in chat.
    Points will be removed from the user at this time. Points ARE refundable

    Can be shortcutted by using !pool <number>
    Aliases available: deposit, spend, donate, contribute (i.e !pool spend)
    Default permission: Everyone
    Example: !pool add 123

!pool commit
    Clears the current donation goal and removes all contribution history. As a safety mechanism, this command must be run twice to actually clear the goals

    Aliases available: clear, reset
    Default Permission: Editor

!pool goal <some goal>
    Sets the current donation goal

    Aliases available: title
    Default Permission: Editor
    Example: !pool goal A brand new car
    Note: When "Setting goal should reset pool" is enabled, the user will NOT be prompted to confirm.

!pool remove <amount>
!pool remove <viewer> <amount>
    Refunds a donation to the viewer. The viewer can only refund the points they've contributed

    Optionally, editors can refund donations to other viewers, say if the donation was done by accident

    Aliases available: withdraw, subtract, sub, undo, refund
    Examples: !pool remove 123, !pool remove Viewer 123

!pool target <number>
    Sets the donation target amount

    Aliases available: goalamount, amount
    Default Permission: editor
    Example: !pool target 1000

!pool top [number]
    Displays the top 3 (by default) contributors

    Aliases available: leaders, leaderboard
    Default permission: everyone
    Example: !pool top 3

!pool transfer <source viewer> <destination viewer>
    Transfers all currency contributions from one viewer to another. The intended use case of this is if the user changes their name.

    Aliases available:
    Default Permission: editor
    Example: !pool transfer oldUser newUser