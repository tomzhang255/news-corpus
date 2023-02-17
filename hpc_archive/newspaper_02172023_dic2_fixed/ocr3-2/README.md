Batch compute all documents

- only outer-most layer has parallel pool
- inner layer has two for-loops with no parallel pool
- use random samples
- each res*.csv has 20 million rows
- each ocr script can only process 2 million rows, and it takes 4+ days



* Problems: incorrect time estimation?
    - took 2 days, but only got to row 75,000 out of 1,000,000 and encounter "cannot split float" error
    - should split into smaller pieces: 100,000, not 1 million
