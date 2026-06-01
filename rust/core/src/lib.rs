//! issues_per_mile = issues / miles for aligned arrays.

pub fn issues_per_mile(issues: &[f64], miles: &[f64]) -> Vec<f64> {
    assert_eq!(issues.len(), miles.len());
    issues
        .iter()
        .zip(miles)
        .map(|(&iss, &mi)| {
            if mi.abs() < 1e-12 {
                0.0
            } else {
                iss / mi
            }
        })
        .collect()
}
