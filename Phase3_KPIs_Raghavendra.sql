CREATE DATABASE indiakart_analytics;
USE indiakart_analytics;
select count(*) from `customers da`;
select count(*) from `orders da`;
select count(*) from `order_items da`;
SELECT COUNT(*) FROM `products da`;
select count(*) from `payments da`;
select count(*) from `returns da`;
SELECT COUNT(*) FROM `inventory da`;
SELECT COUNT(*) FROM `suppliers da`;

SELECT
    status,
    COUNT(*) AS total_orders
FROM `orders da`
GROUP BY status
ORDER BY total_orders DESC;

--  1 total amount of bussiness including cancellations
SELECT
    SUM(final_amount) AS total_gmv
FROM `orders da`;

-- 2  net revenue where orderrs delivered --Sum of final_amount where status = Delivered
SELECT
    SUM(final_amount) AS net_revenue
FROM `orders da`
WHERE status = 'Delivered';

-- 3 Higher AOV = customers buying more per visit (average order value of delivered orders)
SELECT
    SUM(final_amount) / COUNT(*) AS average_order_value
FROM `orders da`
WHERE status = 'Delivered';

-- 4 Target < 10%. Higher = lost revenue
SELECT
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0
    / COUNT(*) AS cancellation_rate_percent
FROM `orders da`;

-- 5 to find return percentage
SELECT
    (SELECT COUNT(*) FROM `returns da`) * 100.0
    / (SELECT COUNT(*) FROM `orders da`
       WHERE status = 'Delivered') AS return_rate_percent;
       
-- 6 Avg total_spent per customer segment for prium segment should be 3x than regular
SELECT
    segment,
    AVG(total_spent) AS average_customer_lifetime_value
FROM `customers da`
GROUP BY segment
ORDER BY average_customer_lifetime_value DESC;

-- to know monthly gmv
SELECT
    DATE_FORMAT(
        STR_TO_DATE(order_date, '%d-%m-%Y'),
        '%Y-%m'
    ) AS order_month,
    SUM(final_amount) AS monthly_gmv
FROM `orders da`
GROUP BY order_month
ORDER BY order_month;

--  7 Calculates monthly GMV and the percentage change from the previous month.
WITH monthly_gmv AS (
    SELECT
        DATE_FORMAT(
            STR_TO_DATE(order_date, '%d-%m-%Y'),
            '%Y-%m'
        ) AS order_month,
        SUM(final_amount) AS gmv
    FROM `orders da`
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(gmv, 2) AS monthly_gmv,
    ROUND(
        (gmv - LAG(gmv) OVER (ORDER BY order_month))
        * 100.0
        / NULLIF(LAG(gmv) OVER (ORDER BY order_month), 0),
        2
    ) AS mom_growth_percent
FROM monthly_gmv
ORDER BY order_month;

-- 8 Top Category Revenue Share
SELECT
    category,
    ROUND(SUM(total_price), 2) AS category_revenue,
    ROUND(
        SUM(total_price) * 100.0
        / (SELECT SUM(total_price)
           FROM `order_items da`),
        2
    ) AS revenue_share_percent
FROM `order_items da`
GROUP BY category
ORDER BY category_revenue DESC;

-- 9 Payment Failure Rate

SELECT
    COUNT(*) AS total_payments,
    SUM(
        CASE
            WHEN status = 'Failed' THEN 1
            ELSE 0
        END
    ) AS failed_payments,
    ROUND(
        SUM(
            CASE
                WHEN status = 'Failed' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS payment_failure_rate_percent
FROM `payments da`;

-- 

SELECT
    status,
    COUNT(*) AS total_skus
FROM `inventory da`
GROUP BY status
ORDER BY total_skus DESC;


SELECT
    COUNT(*) AS total_skus,
    SUM(CASE WHEN status = 'In Stock' THEN 1 ELSE 0 END)
        AS in_stock_skus,
    ROUND(
        SUM(CASE WHEN status = 'In Stock' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS inventory_fill_rate_percent
FROM `inventory da`;

