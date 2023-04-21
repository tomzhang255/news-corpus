List of sub directories, in chronological order of when they're created:

- clean*
- word_count*
- concat
- stat*
- ccr*
- ocr*
- dic*

Description:

- clean*: cleans the original raw html files, extract all the text, put them into a giant csv file. The final csv file would have "file path identifier" mapped with "document text content". Note that a single file is too big to handle, so we've split it up into chunks; each chunk now has 20 million documents (out of ~230 million)
- word_count*: word counts each document, using the cleaned-up csv files.
- concat*: not essential; basically concatenates all the word_count csv results into one.
- stat*: some statistics.
- ccr*: apply the CCR algorithm to a subset of the corpus.
- ocr*: apply post-OCR correction to the corpus. We've only included the processing scripts for one chunk (20 million documents) here.
- dic*: dictionary-based word counting approach; to compare with CCR.
    - in dic6_individualism: the workflow was slightly more automated; we simply need to edit `config.json` and upload a new dictionary to `data/` to count a different dictionary; no need to edit python code.

All the resulting datasets from running these scripts are stored on the HPC:

Go to this directory (`/n/henrich_lab/Lab`), you should then see a few sub folders (`clean`, `ocr`, `ccr`, etc.).
