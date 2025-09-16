SELECT * FROM Stroke.fact_stroke;
-- EDA 初步統計
-- 1.中風和沒有中風的數量
SELECT stroke, COUNT(*) AS count
FROM fact_stroke
GROUP BY stroke;
-- 結果：中風249 沒有中風4861

-- 2. 中風男女比例
SELECT gender, COUNT(*) AS count
FROM fact_stroke
WHERE stroke = 1
GROUP BY gender;
-- 結果：男性中風108 女性中風141

-- 3. 各年龄区间的中风几率（由高到低排序）
SELECT
    age_group,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY age_group
ORDER BY stroke_rate_pct DESC;


-- 高血压 vs 无高血压的中风占比
SELECT
    CASE WHEN hypertension = 1 THEN '有高血壓' ELSE '無高血壓' END AS hypertension_status,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY hypertension_status
ORDER BY stroke_rate_pct DESC;

-- 心脏病 vs 无心脏病的中风占比
SELECT
    CASE WHEN heart_disease = 1 THEN '有心臟病' ELSE '無心臟病' END AS heart_disease_status,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY heart_disease_status
ORDER BY stroke_rate_pct DESC;

-- 已婚 vs 未婚的中风占比
SELECT
    ever_married,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY ever_married
ORDER BY stroke_rate_pct DESC;

-- 工作类型对中风的影响（自營業者、私營、政府、小孩、無業）
SELECT
    work_type,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY work_type
ORDER BY stroke_rate_pct DESC;

-- 居住环境对中风的影响（城市 vs 鄉村）
SELECT
    residence_type,
    COUNT(*) AS total_count,
    SUM(stroke) AS stroke_count,
    ROUND(SUM(stroke) / COUNT(*) * 100, 2) AS stroke_rate_pct
FROM Stroke.fact_stroke
GROUP BY residence_type;

