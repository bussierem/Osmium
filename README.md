# Osmium ![alt text](https://github.com/bussierem/Osmium/blob/master/icons/osmium.ico "Osmium Logo")

Osmium is intended to be a combination learning experience and new file explorer for me (and possibly others) to use.  My intent is to mimic the basics of any normal file explorer (and in the process learn more about how they work), and then add some stuff that I've felt is missing from the standard file explorers.

This is being written in Python, with Tkinter being used for the UI work.  My intent is to have a database of some kind eventually (not sure which one yet) to support certain features.

The current plan is to create the MVP (Minimum Viable Product) to replicate the essentials of a file browser.  Once that is complete, I will be adding several features from my own personal wishlist.  After those are complete I will be taking requests on other possible features.

---

### Minimum Viable Product Features
These are the features that, when complete, will represent what I consider to be a "barebones file explorer".  This feature list will be sporadic in nature and varying in specificity - just things I think of as I code.
  - ~~Basic folder/file navigation~~
    - Order items by folder (alphabetically), then by item (alphabetically)
  - ~~File/etc Menu~~
    - **NOTE:** Most of the menu options will not be implemented in the MVP
  - ~~"URL" path navigation bar~~
  - ~~Buttons:~~
    - ~~Back~~
    - ~~Forward~~
    - ~~"Up One Level"~~
  - ~~Open files with default OS app~~
  - ~~Tree sidebar navigation~~
  - Search Bar
  - ~~Icons for files/folders in main view~~
  - Right-click menu
    - ~~Cut/Copy/Paste~~
        - Solve problems with Copy/Paste threading
        - Why is Windows Explorer crashing sometimes when I do this?
    - ~~Delete (with confirm)~~
        - ~~This goes to Recycle Bin~~
    - ~~Rename (popup with name and ext options)~~
    - ~~Bookmarking~~
        - ~~Drag-and-drop reordering for Bookmarks~~
    - ~~Tag (Not implemented in MVP)~~
    - Properties
  - ~~Confirm popup on Shift+Delete~~
  - "Properties" popup window 

---

### Extra Features
These are features that I will only start looking at or considering after I have the aforementioned MVP completed.
  - "Tagging" of files/folders
    - Right-Click/Menu functionality
  - Tabbed Navigation
    - Chrome-style shortcut keys for navigating tabs
        - Don't forget Ctrl+# to navigate to the #th Tab!
  - Determine and add some right-click menu for the column headers
  - Remove File Menu
    - Replace with F1 "Help" showing keyboard shortcuts
    - Create "Settings" button in Bookmarks Bar
  - User created bookmarks
    - Chrome-style "Bookmarks Bar"
  - Indexing/Caching for better Search performance
  - Advanced Searching
    - Search contents of files
    - Prioritize tagged files
  - Optimizing performance
  - "Open With" Option
  - Allow "delete confirmation" popup to be disabled via checkbox on popup
    - by filetype or location advanced disable?
  - Add "Recycle instead" option to "delete confirmation" popup
