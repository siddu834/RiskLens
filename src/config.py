import os

RANDOM_SEED = 42
# Bound parallelism on laptops; override explicitly for larger machines.
N_JOBS = int(os.environ.get("RISKLENS_N_JOBS", "2"))
if N_JOBS < 1:
    raise ValueError("RISKLENS_N_JOBS must be a positive integer")
TEST_SIZE = 0.20
N_FOLDS = 5
TARGET_COL = "SeriousDlqin2yrs"
DATA_PATH = "data/cs-training.csv"
DEV_PATH = "data/dev.csv"
TEST_PATH = "data/test.csv"
