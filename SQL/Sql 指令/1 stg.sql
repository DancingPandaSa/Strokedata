use Stroke;
select * from strokedata;
DESCRIBE strokedata;
SELECT
    SUM(CASE WHEN bmi = 'N/A' THEN 1 ELSE 0 END) AS bmi_NA_count,
    SUM(CASE WHEN avg_glucose_level = 'N/A' THEN 1 ELSE 0 END) AS glucose_NA_count
FROM strokedata;

DROP TABLE IF EXISTS stg_strokedata;

CREATE TABLE stg_strokedata AS
SELECT
    id,
    gender,
    CAST(age AS UNSIGNED) AS age,
    hypertension,
    heart_disease,
    ever_married,
    work_type,
    Residence_type AS residence_type,
    CASE
        WHEN TRIM(avg_glucose_level) = 'N/A' THEN NULL
        ELSE CAST(TRIM(avg_glucose_level) AS DOUBLE)
    END AS avg_glucose_level,
    CASE
        WHEN TRIM(bmi) = 'N/A' THEN NULL
        ELSE CAST(TRIM(bmi) AS DOUBLE)
    END AS bmi,
    smoking_status,
    CASE WHEN stroke = 1 THEN TRUE ELSE FALSE END AS stroke
FROM
    (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY id) AS row_num
        FROM
            strokedata
    ) AS subquery
WHERE
    subquery.row_num = 1
    AND CAST(subquery.age AS UNSIGNED) > 0
    AND CAST(subquery.age AS UNSIGNED) <= 120;
    
SELECT * FROM stg_strokedata
LIMIT 10;

SELECT id, COUNT(*) FROM stg_strokedata
GROUP BY id
HAVING COUNT(*) > 1;

SELECT id, age FROM stg_strokedata
WHERE age <= 0 OR age > 120;

-- 检查是否有'N/A'字符串
SELECT
    SUM(CASE WHEN bmi = 'N/A' THEN 1 ELSE 0 END) AS bmi_NA_count,
    SUM(CASE WHEN avg_glucose_level = 'N/A' THEN 1 ELSE 0 END) AS glucose_NA_count
FROM stg_strokedata;

-- 或者，更准确地检查NULL值
SELECT
    SUM(CASE WHEN bmi IS NULL THEN 1 ELSE 0 END) AS bmi_null_count,
    SUM(CASE WHEN avg_glucose_level IS NULL THEN 1 ELSE 0 END) AS glucose_null_count
FROM stg_strokedata;

SELECT
    AVG(bmi) AS median_bmi
FROM (
    SELECT
        bmi,
        ROW_NUMBER() OVER (ORDER BY bmi) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM
        stg_strokedata
    WHERE
        bmi IS NOT NULL
) AS subquery
WHERE
    subquery.row_num = FLOOR(subquery.total_count / 2) + 1
    OR subquery.row_num = CEIL(subquery.total_count / 2);
SET SQL_SAFE_UPDATES = 0;

UPDATE stg_strokedata
SET bmi = (
    SELECT median_bmi
    FROM (
        SELECT
            AVG(t1.bmi) AS median_bmi
        FROM (
            SELECT
                bmi,
                ROW_NUMBER() OVER (ORDER BY bmi) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM
                stg_strokedata
            WHERE
                bmi IS NOT NULL
        ) AS t1
        WHERE
            t1.row_num = FLOOR(t1.total_count / 2) + 1
            OR t1.row_num = CEIL(t1.total_count / 2)
    ) AS median_subquery
)
WHERE bmi IS NULL;

SET SQL_SAFE_UPDATES = 1; -- Re-enable safe mode when you're done

SELECT * FROM stg_strokedata;