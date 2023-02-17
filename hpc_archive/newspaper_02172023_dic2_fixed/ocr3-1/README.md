Batch compute all documents

- only outer-most layer has parallel pool
- inner layer has two for-loops with no parallel pool
- use random samples
- each res*.csv has 20 million rows
- each ocr script can only process 2 million rows, and it takes 4+ days
