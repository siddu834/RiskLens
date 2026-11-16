"""Run selected notebooks with this Python environment, preserving execution evidence."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.platform == 'win32':
        # ZMQ needs add_reader; avoid an extra selector thread during shutdown.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebooks', nargs='+', choices=[f'{i:02}' for i in range(9)],
                        default=[f'{i:02}' for i in range(9)])
    args = parser.parse_args()
    run_dir = ROOT / '.runs'
    kernel_dir = run_dir / 'kernels' / 'python3'
    kernel_dir.mkdir(parents=True, exist_ok=True)
    (kernel_dir / 'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'RiskLens reproduction', 'language': 'python'
    }), encoding='utf-8')
    for variable in ['OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        os.environ.setdefault(variable, '1')
    os.environ.setdefault('OMP_NUM_THREADS', '2')
    os.environ.setdefault('LOKY_MAX_CPU_COUNT', '2')
    os.environ['JUPYTER_PATH'] = str(run_dir)
    for variable, subdirectory in [('IPYTHONDIR', 'ipython'),
                                   ('JUPYTER_RUNTIME_DIR', 'runtime'),
                                   ('MPLCONFIGDIR', 'matplotlib')]:
        os.environ[variable] = str(run_dir / subdirectory)
    import nbformat
    from nbclient import NotebookClient
    for prefix in args.notebooks:
        notebook = next((ROOT / 'notebooks').glob(prefix + '_*.ipynb'))
        document = nbformat.read(notebook, as_version=4)
        for cell in document.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        started = time.monotonic()
        print('Running', notebook.name, flush=True)
        client = NotebookClient(document, timeout=7200, kernel_name='python3',
                                resources={'metadata': {'path': str(ROOT / 'notebooks')}})
        try:
            client.execute()
        finally:
            nbformat.write(document, run_dir / notebook.name)
        result = {'notebook': notebook.name, 'status': 'passed',
                  'seconds': round(time.monotonic()-started, 2)}
        with (run_dir / 'runs.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(result)+'\n')
        print(result, flush=True)


if __name__ == '__main__':
    main()
