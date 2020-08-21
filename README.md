# Zotero Remarkable Sync

This is a little utility that made by [Oscar Morrison](https://github.com/oscarmorrison/zoteroRemarkable) to keep a collection/folder in sync with Zotero and Remarkable. This fork makes it more Pythonic, easier to install, and works for me (while the initial version did not work with my Zotero version).

## Setup
 - Install [rmapi](https://github.com/juruen/rmapi), the Go tool that interfaces with reMarkable
 - Install this repo with `pip3 install git+https://github.com/martinosorb/zoteroRemarkable.git`
 - Create a `config.ini` file modelled on the example in the `zoteroRemarkable` folder.

### Env file
- Create a zotero api key
- get zotero library_id (from zotero web)
- create a folder on remarkable and a collection in zotero
- get base path for zotero pdf (papers)

### Usage
_(Ensure you have a config file, with zotero api key, and rmapi setup)_  
Then to sync, at any time from any folder, just run:  
  `python3 -m zoteroRemarkable`
