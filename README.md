## Wiki-Extractor
This is a simple GUI tool completely written in Python which extracts data from Wikipedia.
It uses [wikipedia](https://pypi.org/project/wikipedia/) module to get data and [tkinter](https://docs.python.org/3/library/tk.html) to show it to you.
You can also save the data in a text or PDF file (requires [FPDF](https://pypi.org/project/fpdf/)) and also search for related keywords.

## Details
Wiki-Extractor uses [wikipedia](https://pypi.org/project/wikipedia/) module to get the data related to given word and also get some related keywords.
In order to speed up this process and provide good user experience:
- It uses cache to store the fetched data.
- It uses threading so that the GUI doesn't freeze while searching for the keyword.

## Requirements
- Python3 (or above)
- [wikipedia](https://pypi.org/project/wikipedia/)
- [tkinter](https://docs.python.org/3/library/tk.html)
- [FPDF](https://pypi.org/project/fpdf/)

## How to use
With all the requirements fulfilled, you just need to run the script:

`python3 wiki_extractor.py`

and the GUI will open. Just enter the word you want to search for and hit Enter or click Search Button.
After a few seconds, result will be in the Text box and some related words in the list.
If you want to search for an item from the list, simply click on that item and the tool will search for it. To save the data, click on the `Text file` or `PDF file` button.
