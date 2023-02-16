Batch compute all documents

- only outer-most layer has parallel pool
- inner layer has two for-loops with no parallel pool
- each job only processes 100,000 documents

- new problem: still memory allocaiton error with Pool()
    - potential fix: use `forkserver` or `spawn` instead of `fork` as start method
    - need to test this - still does not work
- new plan: do not use pool at all, just sequential: 1000 rows ~ 2.5 minutes
