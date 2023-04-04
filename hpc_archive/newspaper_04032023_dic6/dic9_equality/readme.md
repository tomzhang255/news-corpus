- dictionary word counting on OCR processed text
- partitions 9, 10, 11 are not further split into chunks
- for partitions 0-8, each has <= 20 chunks

- new since dic5: now using `config.json` to not repeat too much work
- now everytime we need to count a new dictionary, do the following
    - upload dictionary to `data/`
    - edit `config.json`
    - run `all.sh` with `. all.sh > all.txt`
