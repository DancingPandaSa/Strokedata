SELECT * FROM Stroke.int_strokedata;
DROP TABLE IF EXISTS fact_stroke;
CREATE TABLE fact_stroke AS
SELECT
    id AS fact_id,
    age,
    age_group,
    bmi,
    bmi_category,
    avg_glucose_level,
    glucose_level_category,
    hypertension,
    heart_disease,
    stroke
FROM int_strokedata;
-- 人口维度
DROP TABLE IF EXISTS dim_patient;
CREATE TABLE dim_patient AS
SELECT DISTINCT
    id AS patient_key,
    gender,
    age,
    age_group
FROM int_strokedata;

-- 健康维度
DROP TABLE IF EXISTS dim_health;
CREATE TABLE dim_health AS
SELECT DISTINCT
    id AS health_key,
    hypertension,
    heart_disease,
    bmi,
    bmi_category,
    avg_glucose_level,
    glucose_level_category
FROM int_strokedata;

-- 生活方式维度
DROP TABLE IF EXISTS dim_lifestyle;
CREATE TABLE dim_lifestyle AS
SELECT DISTINCT
    id AS lifestyle_key,
    ever_married,
    work_type,
    residence_type,
    smoking_status
FROM int_strokedata;
DROP TABLE IF EXISTS mart_stroke_features;
CREATE TABLE mart_stroke_features AS
SELECT
    id AS patient_id,
    gender,
    age,
    age_group,
    hypertension,
    heart_disease,
    bmi,
    bmi_category,
    avg_glucose_level,
    glucose_level_category,
    ever_married,
    work_type,
    residence_type,
    smoking_status,
    stroke
FROM int_strokedata;
