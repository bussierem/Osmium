# Osmium ![alt text](https://github.com/bussierem/Osmium/blob/master/resources/icons/osmium.ico "Osmium Logo")

Osmium is intended to be a combination learning experience and new file explorer for me (and possibly others) to use.  My intent is to mimic the basics of any normal file explorer (and in the process learn more about how they work), and then add some stuff that I've felt is missing from the standard file explorers.

This is being written in Python, with Tkinter being used for the UI work.  My intent is to have a database of some kind eventually (not sure which one yet) to support certain features.

The current plan is to create the MVP (Minimum Viable Product) to replicate the essentials of a file browser.  Once that is complete, I will be adding several features from my own personal wishlist.  After those are complete I will be taking requests on other possible features.

---

### Missing Features Before Beta Testing
  - File Transfer Problems:
    - Something causes Windows Explorer to crash sometimes when doing long copy/pasts
    - Need a "progress tacker" window to popup on file transfers
  - Search Problems:
    - If closing the app mid-search, the app leaves a thread running for some reason
    - Options for displaying results:
        - Dynamic updating of the file_explorer (CURRENT)
            - PRO:  Smooth display of results
            - CON:  Threading causing issues
        - Popup progress window then display results all at once
            - PRO:  Probably won't cause the same threading issues
            - CON:  User might continue browsing then be interrupted by results
        - Open results in new window/tab
            - PRO:  Won't cause threading issues
            - PRO:  Doesn't interrupt user
            - CON:  Some people want results in same view
            - CON:  "New Tab" would require implementing tabs for beta
  - Drag-n-Drop
    - Moving files/folders in the file_explorer view
        - Should highlight the hovered row
    - When file/folder is dropped on a folder, it should "move" the target to the destination
  - Multi-Window
    - Drag-n-Drop between windows
    - All windows should update when the other(s) do something
        - "Update" method that runs on a timer
  - Extensive Debug Logging for Beta Testing
    - Option to disable logging actual file/folder paths (for privacy)

---

### Completed Features

These are the features that, when complete, will represent what I consider to be a "barebones file explorer".  This feature list will be sporadic in nature and varying in specificity - just things I think of as I code.
  - ~~Basic folder/file navigation~~
    - ~~Order items by folder (alphabetically), then by item (alphabetically)~~
  - ~~File/etc Menu~~
    - **NOTE:** Most of the menu options will not be implemented in the MVP
  - ~~"URL" path navigation bar~~
  - ~~Buttons:~~
    - ~~Back~~
    - ~~Forward~~
    - ~~"Up One Level"~~
  - ~~Open files with default OS app~~
  - ~~Tree sidebar navigation~~
  - ~~Search Bar~~
  - ~~Icons for files/folders in main view~~
  - ~~Right-click menu~~
    - ~~Cut/Copy/Paste~~
    - ~~Delete (with confirm)~~
        - ~~This goes to Recycle Bin~~
    - ~~Rename (popup with name and ext options)~~
    - ~~Bookmarking~~
        - ~~Drag-and-drop reordering for Bookmarks~~
    - ~~Tag (Not implemented in MVP)~~
    - ~~Properties~~
  - ~~Confirm popup on Shift+Delete~~
  - ~~"Properties" popup window~~
    - ~~Type~~
    - ~~Size~~
        - ~~Handle recursive folder sizes~~
            - ~~Create thread to calculate, query every second and update window~~
        - **Thanks to Supermaik for suggestion on text coloring for dynamic updated properties!**
    - ~~Contents (folders)~~
    - ~~Opens With (files)~~
    - ~~Location~~
    - ~~Creation Date~~
    - ~~Last Modified Date~~

---

### Extra Features
These are features that I will only start looking at or considering after I have the aforementioned MVP completed.
  - "Tagging" of files/folders
    - Right-Click/Menu functionality
  - Tabbed Navigation
    - Chrome-style shortcut keys for navigating tabs
        - Don't forget Ctrl+# to navigate to the #th Tab!
    - Reorder Tabs
    - Drag-n-Drop files over tabs to switch to that tab
    - Pull out tabs as new windows
    - Drag Windows into others to make them into tabs in the destination window
  - Determine and add some right-click menu for the column headers
  - Remove File Menu
    - Replace with F1 "Help" showing keyboard shortcuts
    - Create "Settings" button in Bookmarks Bar
  - User created bookmarks
    - Chrome-style "Bookmarks Bar"
  - Settings
    - Allow "sort by filename", not folders first
  - Indexing/Caching for better Search performance
  - Advanced Searching
    - Search contents of files
    - Prioritize tagged files
  - Optimizing performance
  - "Open With" Option
  - Allow "delete confirmation" popup to be disabled via checkbox on popup
    - by filetype or location advanced disable?
  - Add "Recycle instead" option to "delete confirmation" popup
