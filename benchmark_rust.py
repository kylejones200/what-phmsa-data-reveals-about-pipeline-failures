#!/usr/bin/env python3
import time, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/"src"))
from compute_kernel import issues_per_mile
def main():
    i=np.arange(10000,dtype=float); m=10+i; issues_per_mile(i,m)
    t0=time.perf_counter()
    for _ in range(2000 if "issues_per_mile"=="cyclical_time_features" else 200):
        i=np.arange(10000,dtype=float); m=10+i; issues_per_mile(i,m)
    py_s=time.perf_counter()-t0
    try:
        import what_phmsa_data_reveals_about_pipeline_failures_rs as rs
    except ImportError:
        print("Build: cd rust && maturin develop --release -m py/Cargo.toml"); print(f"Python {py_s:.3f}s"); return
    rs_s=rs.bench_kernel_py(i,m,100000)
    print(f"Python {py_s:.3f}s Rust {rs_s:.3f}s speedup {py_s/max(rs_s,1e-9):.1f}x")
    np.testing.assert_allclose(i, np.asarray(rs.issues_per_mile_py(i,m))[0] if isinstance(rs.issues_per_mile_py(i,m), tuple) else rs.issues_per_mile_py(i,m), rtol=1e-10)
    print("Correctness: OK")
if __name__=="__main__": main()
