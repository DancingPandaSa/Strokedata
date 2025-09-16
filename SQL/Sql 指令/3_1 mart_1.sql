SELECT * FROM Stroke.int_strokedata;
DROP TABLE IF EXISTS mart_age_summary;

CREATE TABLE mart_age_summary AS
SELECT
    age_group,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) AS stroke_count,
    COUNT(*) AS total_count,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) / COUNT(*) AS stroke_rate
FROM
    int_strokedata
GROUP BY
    age_group
ORDER BY
    age_group;

select * from mart_age_summary;

DROP TABLE IF EXISTS mart_bmi_summary;

CREATE TABLE mart_bmi_summary AS
SELECT
    bmi_category,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) AS stroke_count,
    COUNT(*) AS total_count,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) / COUNT(*) AS stroke_rate
FROM
    int_strokedata
GROUP BY
    bmi_category
ORDER BY
    FIELD(bmi_category, 'underweight', 'normal', 'overweight', 'obese');

select * from mart_bmi_summary;

DROP TABLE IF EXISTS mart_glucose_summary;

CREATE TABLE mart_glucose_summary AS
SELECT
    glucose_level_category,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) AS stroke_count,
    COUNT(*) AS total_count,
    SUM(CASE WHEN stroke = TRUE THEN 1 ELSE 0 END) / COUNT(*) AS stroke_rate
FROM
    int_strokedata
GROUP BY
    glucose_level_category
ORDER BY
    FIELD(glucose_level_category, 'normal', 'pre-diabetic', 'high', 'very-high');

select * from mart_glucose_summary;
