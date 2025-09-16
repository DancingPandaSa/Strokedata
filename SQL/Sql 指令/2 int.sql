use Stroke;
SELECT * FROM stg_strokedata;
DROP TABLE IF EXISTS int_strokedata;

CREATE TABLE int_strokedata AS
SELECT
    *,  -- 保留所有 stg_strokedata 表中的原始字段
    -- 年龄分组
    CASE
        WHEN age BETWEEN 0 AND 14 THEN '0-14'
        WHEN age BETWEEN 15 AND 24 THEN '15-24'
        WHEN age BETWEEN 25 AND 44 THEN '25-44'
        WHEN age BETWEEN 45 AND 64 THEN '45-64'
        WHEN age >= 65 THEN '65+'
        ELSE 'Unknown'
    END AS age_group,
    -- BMI 分类
    CASE
        WHEN bmi < 18.5 THEN 'underweight'
        WHEN bmi BETWEEN 18.5 AND 24.9 THEN 'normal'
        WHEN bmi BETWEEN 25.0 AND 29.9 THEN 'overweight'
        WHEN bmi >= 30.0 THEN 'obese'
        ELSE 'unknown'
    END AS bmi_category,
    -- 血糖分组
    CASE
        WHEN avg_glucose_level < 100 THEN 'normal'
        WHEN avg_glucose_level BETWEEN 100 AND 140 THEN 'pre-diabetic'
        WHEN avg_glucose_level BETWEEN 141 AND 200 THEN 'high'
        WHEN avg_glucose_level > 200 THEN 'very-high'
        ELSE 'unknown'
    END AS glucose_level_category
FROM
    stg_strokedata;
SELECT * FROM int_strokedata;