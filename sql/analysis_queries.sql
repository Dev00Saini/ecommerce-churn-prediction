-- E-Commerce Customer Churn — SQL Analysis Queries
-- Database: data/churn.db | Table: customers

-- 1. Overall churn rate
SELECT ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers;

-- 2. Churn rate by preferred login device
SELECT PreferredLoginDevice, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY PreferredLoginDevice
ORDER BY churn_rate_pct DESC;

-- 3. Churn rate by preferred order category
SELECT PreferedOrderCat, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY PreferedOrderCat
ORDER BY churn_rate_pct DESC;

-- 4. Does filing a complaint predict churn?
SELECT Complain, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY Complain;

-- 5. Churn rate by satisfaction score
SELECT SatisfactionScore, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY SatisfactionScore
ORDER BY SatisfactionScore;

-- 6. Avg tenure, order count, and cashback: churned vs retained
SELECT Churn,
       ROUND(AVG(Tenure),1) AS avg_tenure_months,
       ROUND(AVG(OrderCount),1) AS avg_order_count,
       ROUND(AVG(CashbackAmount),2) AS avg_cashback,
       ROUND(AVG(DaySinceLastOrder),1) AS avg_days_since_last_order
FROM customers
GROUP BY Churn;

-- 7. Churn rate by city tier
SELECT CityTier, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY CityTier
ORDER BY CityTier;

-- 8. Churn rate by marital status
SELECT MaritalStatus, COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn)/COUNT(*),1) AS churn_rate_pct
FROM customers
GROUP BY MaritalStatus
ORDER BY churn_rate_pct DESC;