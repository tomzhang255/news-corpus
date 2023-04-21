Purpose: apply post-OCR correction method described in this paper, on one of the chunks (chunk 5) (20 million documents).

Run process_coha.py first to obtain coha_dict.csv

1000 documents ~ 2.5 minutes

Do it by batch size of 1 million.

On average, one script (which processes 1 million documents) takes 3-5 days to run; but we can submit multiple jobs on the HPC so they can all run at the same time.
