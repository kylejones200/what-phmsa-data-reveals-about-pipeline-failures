use what_phmsa_data_reveals_about_pipeline_failures_core::issues_per_mile;
fn main() { let i: Vec<f64>=(0..10000).map(|x| x as f64).collect(); let m: Vec<f64>=(0..10000).map(|x| 10.+x as f64).collect(); for _ in 0..100000 { let _=issues_per_mile(&i,&m); } }
