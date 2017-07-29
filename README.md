# evernote2zim
Convert Evernote export to zim-wiki syntax

This is achieved by:

1. Export your evernote docs to html and save to a folder (<HTML_DIR>).
2. Convert html to markdown by using the html2text module.
3. Convert markdown to zim-wiki syntax using the markdown2zim module, and
   save to a given folder <ZIM_DIR>.
4. Copy over attched images to <ZIM_DIR>.
5. In zim desktop, create a new notebook, this will create a new folder
   in your drive. Close the new notebook and go into that folder,
   and copy over the stuff (.txt files and attachment folders)
   to this new folder.
6. Open the new notebook again to see the final result.

Steps 2-4 are done by this script. Other step should be done by the user.


# Usage

```
python evernote2zim.py HTML_DIR ZIM_DIR
```


Some tips:

* After creating the new notebook, you can let it stay open, and
  copy over the docs, then use Tools -> Update index to let
  it refresh.
* Sometimes after the above the HOME page is gone, try restarting
  zim.
* When exporting your docs from Evernote, right click a notebook to
  export the entire notebook.
* These symbols are not allowed in zim's note title:
    ```
    #, *, _, \, |, /, <, >, ?, ", %
    ```
    I changed "%" to "percent", and all others are simply deleted. So be aware that your title might be different from in   Evernote.
      
* Still rather early stage so probably a bit buggy. Let me know if you encounter one.
* Also, don't use zim-wiki 0.66. It's buggy as hell. Fall back to 0.65 until they fix things up. Spell checking in 0.67 also doesn't work for me.

# Dependencies

* Python: only tested python2.


# Related projects

* [zim-wiki](http://zim-wiki.org/)
* [markdown2zim](https://github.com/Xunius/markdown2zim), which is modified from [python-markdown2](https://github.com/trentm/python-markdown2).
* [html2text](https://github.com/aaronsw/html2text).

