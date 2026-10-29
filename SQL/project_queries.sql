# customer churn prediction using ML, users data analysis

use netflix;
select * from users;

-- 1. Total number of customers
select count(*) as Total_Customers
from users;

-- 2. Number of churned customers
select count(*) as Churned_Customers
from users
where churn = 1;

-- 3. Number of active customers
select count(*) as Active_Customers
from users
where is_active = "True";

-- 4. Customers by subscription plan
select subscription_plan, count(*) as total
from users
group by subscription_plan;

-- 5. Average monthly charge
select avg(Monthly_Charge) as Avg_Charge
from users;

-- 6. Average customer age
select avg(age) as Average_Age
from users;

-- 7. Customers by gender
select gender, count(*) as Total
from users
group by gender;

-- 8. Customers by country
select country, count(*) as Total
from users
group by country;

-- 9. Customers using each device
select primary_device, count(*) as Users
from users
group by primary_device;

-- 10. Auto-renew enabled vs disabled
select auto_renew, count(*) as Users
from users
group by auto_renew;



-- 11. Churn rate by subscription plan
select subscription_plan,
count(*) as Total_Customers,
sum(churn) as Churned_Customers
from users
group by subscription_plan;

-- 12. Average watch hours by churn status
select churn,
avg(watch_hours_L30_days) as Avg_Watch_Hours
from users
group by churn;

-- 13. Average monthly charge of churned customers
select avg(Monthly_Charge)
from users
where churn = 1;

-- 14. Customers with payment failures
select *
from users
where payment_failures > 1;

-- 15. Churned customers with payment failures
select count(*)
from users
where churn = 1
and payment_failures > 0;

-- 16. Average account age by churn status
select churn,
avg(account_age_days)
from users
group by churn;

-- 17. Customers inactive for more than 30 days
select *
from users
where days_since_last_login > 30;

-- 18. Top 10 highest paying customers
select user_id,
Monthly_Charge
from users
order by Monthly_Charge DESC
limit 10;

-- 19. Average watch hours by subscription plan
select subscription_plan,
avg(watch_hours_L30_days)
from users
group by subscription_plan;


-- 20. Number of senior users
select count(*)
from users
where senior_user = 1;

-- Business insight Queries 

-- 21. Which subscription plan has the highest churn?
select subscription_plan,
sum(churn) as Churned
from users
group by subscription_plan
order by Churned DESC;

-- 22. Top 10 cities with highest churn
select city,
sum(churn) as Churned
from users
group by city
order by Churned DESC
limit 10;

-- 23. Churn by device
select primary_device,
sum(churn) as Churned
from users
group by primary_device;

-- 24. Customers without auto-renew who churned
select count(*)
from users
where auto_renew = 0
and churn = 1;

-- 25. Average last login days by churn status
select churn,
avg(days_since_last_login)
from users
group by churn;

-- 26. Customers with low watch hours (<10) who churned
select count(*)
from users
where watch_hours_L30_days < 10
and churn = 1;

-- 27. Churn percentage by subscription plan
select subscription_plan,
round(sum(churn)*100.0/count(*),2) as Churn_Percentage
from users
group by subscription_plan;

-- 28. Top 5 states with highest customers
select state_province,
count(*) as Customers
from users
group by state_province
order by Customers DESC
limit 5;

-- 29. Average payment failures by churn status
select churn,
avg(payment_failures)
from users
group by churn;


-- 30. High-value customers who churned
select user_id,
Monthly_Charge,
subscription_plan
from users
where churn = 1
order by Monthly_Charge DESC
limit 10;
