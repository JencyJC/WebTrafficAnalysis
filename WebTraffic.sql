-- CREATE DATABASE web_analysis;

USE web_analysis;

-- CREATE TABLE web_traffic (
--   session_id INTEGER PRIMARY KEY,
--   user_id INT,
--   timestamp DATETIME,
--   page_url VARCHAR(100),
--   source VARCHAR(50),
--   medium VARCHAR(50),
--   device VARCHAR(50),
--   region VARCHAR(50),
--   bounce INT,
--   session_duration INT
-- );

SELECT * FROM web_traffic;

-- SELECT * FROM web_traffic LIMIT 10;

-- DELETE FROM web_traffic;

-- DROP TABLE web_traffic;

-- DROP DATABASE web_traffic;

-- DELETE FROM web_traffic;

SELECT * FROM web_traffic;

-- Analysis

-- Most visited pages
SELECT page_url, COUNT(*) AS visits
FROM web_traffic
GROUP BY page_url
ORDER BY visits DESC
LIMIT 10;


-- Bounce rate by source
SELECT source, 
       SUM(bounce) * 100.0 / COUNT(*) AS bounce_rate
FROM web_traffic
GROUP BY source;


-- Average session duration by device
SELECT device, AVG(session_duration) AS avg_duration
FROM web_traffic
GROUP BY device;


-- To track how many users move from page_url
SELECT page_url, COUNT(DISTINCT session_id) AS Visitors
FROM web_traffic
WHERE page_url IN ('/home', '/product', '/blog', '/contact', '/pricing')
GROUP BY page_url
ORDER BY FIELD(page_url, '/home', '/product', '/blog', '/contact', '/pricing');


-- Top Sources Driving Quality Traffic
SELECT 
  source,
  ROUND(SUM(bounce) * 100.0 / COUNT(*), 2) AS bounce_rate,
  ROUND(AVG(session_duration), 2) AS avg_duration,
  COUNT(*) AS total_sessions
FROM web_traffic
GROUP BY source
ORDER BY avg_duration DESC;


-- New vs Returning Visitors (if user_id repeats)
SELECT 
  CASE 
    WHEN user_sessions = 1 THEN 'New'
    ELSE 'Returning'
  END AS user_type,
  COUNT(*) AS users
FROM (
  SELECT user_id, COUNT(*) AS user_sessions
  FROM web_traffic
  GROUP BY user_id
) AS session_counts
GROUP BY user_type;


-- Traffic Spike or Drop Detection
SELECT 
  DATE(timestamp) AS visit_date,
  COUNT(*) AS total_sessions
FROM web_traffic
GROUP BY visit_date
ORDER BY total_sessions DESC
LIMIT 3;
