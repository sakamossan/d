CREATE VIEW IF NOT EXISTS girl_stat AS SELECT
  db_girl.*,
  SUM(wait) wait,
  SUM(work) work,
  ((((("http://www.cityheaven.net/" || scrape_shop.area) || "/") || scrape_shop.id) || "/A6GirlDetailProfile/?girlId=") || db_girl.id) as url
FROM (
    SELECT
      db_attendance.girl_id girl_id,
      CASE db_statuslog.status WHEN 'wait' THEN 1 ELSE 0 END wait,
      CASE db_statuslog.status WHEN 'work' THEN 1 ELSE 0 END work
    FROM
      db_statuslog
    JOIN
      db_attendance ON db_statuslog.attendance_id = db_attendance.id
) t
JOIN
  db_girl ON db_girl.id = t.girl_id,
  scrape_shop ON scrape_shop.id = db_girl.shop_id
GROUP BY t.girl_id;