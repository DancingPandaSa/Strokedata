use Stroke;
select * from strokedata;

-- EDA 初步統計
-- 1.中風和沒有中風的數量
SELECT stroke, COUNT(*) AS count
FROM strokedata
GROUP BY stroke;
-- 結果：中風249 沒有中風4861

-- 2. 中風男女比例
SELECT gender, COUNT(*) AS count
FROM strokedata
WHERE stroke = 1
GROUP BY gender;
-- 結果：男性中風108 女性中風141

-- 3. 中風年齡區間統計
SELECT 
  CASE 
    WHEN age BETWEEN 1 AND 14 THEN '1-14岁'
    WHEN age BETWEEN 15 AND 24 THEN '15-24岁'
    WHEN age BETWEEN 25 AND 44 THEN '25-44岁'
    WHEN age BETWEEN 45 AND 64 THEN '45-64岁'
    WHEN age >= 65 THEN '65岁以上'
  END AS age_group,
  COUNT(*) AS total,
  SUM(stroke) AS stroke_count,
  ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY age_group
ORDER BY stroke_rate DESC;
-- 結果：65歲以上中風 佔比15.48%；45-64歲 佔比5.16%；25-44歲 佔比0.62%； 1-14歲 佔比1.29%；15-24歲 佔比0%



-- 4.高血壓 (hypertension)
SELECT hypertension,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY hypertension
ORDER BY stroke_rate DESC;
-- 結果：有高血壓中風 佔比13.25%；無高血壓中風 3.97%

-- 5.心臟病(heart_disease)
SELECT heart_disease,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY heart_disease
ORDER BY stroke_rate DESC;
-- 結果：有心臟病中風佔比 17.03%； 無心臟病中風4.18%

-- 6.婚姻狀況 (ever_married)
SELECT ever_married,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY ever_married
ORDER BY stroke_rate DESC;
-- 結果：已婚中風 6.56%；未婚中風 1.65%

-- 7.工作類型 (work_type)
SELECT work_type,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY work_type
ORDER BY stroke_rate DESC;
-- 結果：自營業者中風 7.94%；私營 5.09%；政府工作 5.02%； 小孩 0.2%；無業 0%

-- 8.居住類型 (Residence_type)
SELECT Residence_type,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY Residence_type
ORDER BY stroke_rate DESC;
-- 結果:城市中風 5.2%；鄉村 4.53%


-- 9.吸煙狀況 (smoking_status)

SELECT smoking_status,
       COUNT(*) AS total,
       SUM(stroke) AS stroke_count,
       ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY smoking_status
ORDER BY stroke_rate DESC;
-- 結果：有吸煙史者中風 7.91%；吸煙者5.32%；不吸煙者 4.76%；未知 3.04%

-- 10.連續性變量 (血糖 & BMI)
-- 血糖分組
SELECT 
  CASE 
    WHEN avg_glucose_level < 100 THEN '<100'
    WHEN avg_glucose_level BETWEEN 100 AND 140 THEN '100-140'
    WHEN avg_glucose_level BETWEEN 141 AND 200 THEN '141-200'
    ELSE '>200'
  END AS glucose_group,
  COUNT(*) AS total,
  SUM(stroke) AS stroke_count,
  ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY glucose_group
ORDER BY stroke_rate DESC;
-- 結果：血糖>200 中風佔比 12.81%；血糖 141-200之間 9.57%； 血糖 100-140 3.8%；血糖<100 3.58%

-- BMI 分組
SELECT 
  CASE 
    WHEN bmi < 18.5 THEN '偏瘦(<18.5)'
    WHEN bmi BETWEEN 18.5 AND 24.9 THEN '正常(18.5-24.9)'
    WHEN bmi BETWEEN 25 AND 29.9 THEN '超重(25-29.9)'
    ELSE '肥胖(>=30)'
  END AS bmi_group,
  COUNT(*) AS total,
  SUM(stroke) AS stroke_count,
  ROUND(SUM(stroke)/COUNT(*), 4) AS stroke_rate
FROM strokedata
GROUP BY bmi_group
ORDER BY stroke_rate DESC;
-- 結果：BMI<18.5 偏瘦者 中風佔比7.62%; BMI15-29.9 超重者 中風佔比5.32%；BMI>=30 肥胖者 中風佔比5.10%；BMI 18.5-24.9 正常 中風佔比2.82%


