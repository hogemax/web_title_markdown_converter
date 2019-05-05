#web_title_markdown_converter

# Environment

- python3

- need library

```
beautifulsoup4
requests
urllib3
```

# How to use

Scraping single page

```
python py3_get_title.py URL
```

Scraping some pages (from txt-file)

```
python py3_get_title.py file.txt
```

# Ex

- Create necessary file (Be careful about file duplication)

```
cd ~/
touch reference_url_list.txt
```

- Write the following settings to your shell-rc (Please correct if necessary .py-file path)

```
function refgeturls() {
  if [[ -n $1 && $1 =~ _url_list.txt ]]; then
    command pbpaste > $1; command cat $1; command printf "\n---------->>\n"
    command python3 ~/web_title_markdown_converter/py3_get_title.py $1
  else
    echo "Please specify the file to the argument"
  fi
}
```

- Save multiple URLs to the clipboard


- Do it this command (At your own risk)

```
refgeturls reference_url_list.txt
```



