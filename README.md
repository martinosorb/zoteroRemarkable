# Zotero Remarkable Sync

This is a little utility that made by [Oscar Morrison](https://github.com/oscarmorrison/zoteroRemarkable) to keep a collection/folder in sync with Zotero and Remarkable. This fork makes it more Pythonic, easier to install, and works for me (while the initial version did not work with my Zotero version).

## Setup
 - Install [rmapi](https://github.com/juruen/rmapi), the Go tool that interfaces with reMarkable
 - Clone this repo with `git clone https://github.com/martinosorb/zoteroRemarkable.git`
 - Create a `config.ini` file modelled on the example in the `zoteroRemarkable` folder (see below for details).
 - *After* you've created the `config.ini` file, install with pip:
 ```bash
 cd zoteroRemarkable
 pip install .
 ```

### Config file
- Get your Zotero library_id and an API key from [Zotero web](https://www.zotero.org/settings/keys).
- Create a folder on reMarkable and a collection in Zotero, which will be synced to each other.
- Get base path for Zotero PDFs (the storage folder on your local machine, for me this is /Users/johndoe/Documents/Zotero/storage).
- Find the path of your `rmapi` installation.
- Add this information to the `config.ini` file (don't forget to remove `_EXAMPLE` from the name).

### Usage
Ensure you have a config file, with zotero api key, and rmapi setup as described above. Then to sync, at any time from any terminal, just run: `python3 -m zoteroRemarkable`.

Currently, syncing is driven by the Zotero collection, i.e. files present in the collection will be uploaded to the reMarkable, and files _not_ present in the collection but present on the reMarkable _will be deleted from the reMarkable_. Note that this may cause loss of your annotations if you're not careful. I'm working on a better solution.
