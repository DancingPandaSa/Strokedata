SELECT * FROM Stroke.int_strokedata;
DROP TABLE IF EXISTS mart_stroke_age_bmi;
CREATE TABLE mart_stroke_age_bmi AS
SELECT
    age_group,
    bmi_category,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke)/COUNT(*)*100, 2) AS stroke_rate_pct
FROM int_strokedata
GROUP BY age_group, bmi_category
ORDER BY age_group, bmi_category;
DROP TABLE IF EXISTS mart_stroke_gender_smoking;
CREATE TABLE mart_stroke_gender_smoking AS
SELECT
    gender,
    smoking_status,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke)/COUNT(*)*100, 2) AS stroke_rate_pct
FROM int_strokedata
GROUP BY gender, smoking_status
ORDER BY gender, smoking_status;
DROP TABLE IF EXISTS mart_stroke_worktype;
CREATE TABLE mart_stroke_worktype AS
SELECT
    work_type,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke)/COUNT(*)*100, 2) AS stroke_rate_pct
FROM int_strokedata
GROUP BY work_type
ORDER BY stroke_rate_pct DESC;
