use netflix;
-- 1.Total number of customers
select count(*) from users;

-- 2.Number of churned customers
select count(*) as churned_users from users 
where churn=1;

-- 3.Number of active customers
SELECT COUNT(*) AS Active_Customers
FROM users
WHERE churn = 0;

-- 4. Customers by subscription plan
SELECT subscription_plan, COUNT(*) AS Total
FROM users
GROUP BY subscription_plan;

-- 5. Average customer age
select avg(age) as average_age from users;

-- 6. Customers by gender
select gender,count(*) as total
from users
group by gender;

-- 7.Customers by country
select country,count(*) as no_of_users
from users
group by country;

-- 8 Customers using each device
select primary_device,count(*) as device_user
from users 
group by primary_device;

-- 9.Auto-renew enabled vs disabled
select auto_renew,count(*) as auto_renew_users
from users
group by auto_renew;

-- 10.Churn rate by subscription plan
select subscription_plan,count(*) as total_customers,sum(churn) as churned_users
from users
group by subscription_plan;

-- 11.Average watch hours by churn status
select churn,avg(watch_hours_L30_days) from users
group by churn;

-- 12. Customers with payment failures > 2
select * from users
where payment_failures>2;