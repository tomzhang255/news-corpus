The corpus collection is too large; need to access only parts of it at a time, then save it - then move on to the next chunk. Tried using a while loop here, but ran into memory issues.

Solution: Submit separate batch jobs. Each job would only process 20 million rows from the meta data. Run into memory issues for chunks 6 and 7, so we're further separating 6 and 7 into halfs: 6a, 6b, 7a, 7b.

Each job takes within 4 hours to run.
