Purpose: count words in each document from the cleaned-up csv files.

If we load in the entire file all at once: memory issues - cannot load that text column from res csv files.
Need to use chunking instead.

Takes within 4 hours to run each script.

Note that each script counts a chunk of the cleaned data; each chunk has 20 million documents.
