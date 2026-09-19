import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv('retail_sales_dataset.csv')
conn = sqlite3.connect("retail.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

# Total Revenue
print("Total revenue generated:")
q1 = "SELECT SUM(Total_Amount) AS 'Total Revenue' FROM sales"
r1 = pd.read_sql_query(q1, conn)
print(r1.to_string(), "\n")

# Revenue produced by each product category
print("Revenue produced by each product: ")
q2 = "SELECT Product_Category AS 'Category', SUM(Total_Amount) AS 'Revenue' FROM sales GROUP BY Product_Category"
r2 = pd.read_sql_query(q2, conn)
print(r2.to_string(), "\n")

# Product Category with the most units sold
print("Category with most units sold: ")
q3 = "SELECT Product_Category AS 'Category', SUM(Quantity) AS 'Max Units' FROM sales GROUP BY Product_Category ORDER BY SUM(Quantity) DESC"
r3 = pd.read_sql_query(q3, conn)
print(r3, "\n")

# Average Transaction Value for each category
print("Average revenue for each category: ")
q4 = "SELECT Product_Category AS 'Category', AVG(Total_Amount) AS 'Average' FROM sales GROUP BY Product_Category"
r4 = pd.read_sql_query(q4, conn)
print(r4, "\n")

# What age group spends the most?
print("Age group spending the most: ")
q5 = "SELECT SUM(Total_Amount) AS 'Total', CASE WHEN Age BETWEEN 18 AND 25 THEN '18-25' WHEN Age BETWEEN 26 AND 35 THEN '26-35' WHEN Age BETWEEN 36 AND 45 THEN '36-45' WHEN Age BETWEEN 46 AND 55 THEN '46-55' ELSE '55+' END AS 'Age_Group' FROM sales GROUP BY Age_Group ORDER BY Total DESC"
r5 = pd.read_sql_query(q5, conn)
print(r5, "\n")

r5.plot(x="Age_Group", y='Total', kind="bar")
plt.title("Age Groups VS Spending")
plt.xlabel("Age Group")
plt.ylabel("Revenue Spent")
plt.show()

# Spending Difference between Genders
print("Difference in spending between male and female: ")
q6 = "SELECT Gender, SUM(Quantity) AS 'Total Units Sold', SUM(Total_Amount) AS 'Total Revenue', AVG(Total_Amount) AS 'Average Revenue' FROM sales GROUP BY Gender"
r6 = pd.read_sql_query(q6, conn)
print(r6, "\n")

# Monthly Sales Trend
print("Monthly Sales Trend: ")
q7 = "SELECT strftime('%m', SUBSTR(Date, 7, 4) || '-' || SUBSTR(Date, 4, 2) || '-'  || SUBSTR(Date, 1, 2)) AS 'Month', SUM(Total_Amount) AS 'Total' FROM sales GROUP BY Month"
r7 = pd.read_sql_query(q7, conn)
print(r7, "\n")

r7.plot(x="Month", y="Total", kind="line")
plt.title("Monthly Sales Trend")
plt.xlabel("Months")
plt.ylabel("Total Revenue")
plt.show()

# Month-over-Month Revenue Growth
print("Monthly Revenue Growth: ")
q8 = "SELECT Month, Total, Total - LAG(Total) OVER (ORDER BY Month) AS 'Revenue Change' FROM (SELECT strftime('%m', SUBSTR(Date, 7, 4) || '-' || SUBSTR(Date, 4, 2) || '-'  || SUBSTR(Date, 1, 2)) AS 'Month', SUM(Total_Amount) AS 'Total' FROM sales GROUP BY Month) ORDER BY Month"
r8 = pd.read_sql_query(q8, conn)
print(r8, "\n")

r8.plot(x="Month", y="Revenue Change", kind="line")
plt.title("Monthly Revenue Change")
plt.xlabel("Months")
plt.ylabel("Change in Revenue")
plt.show()

# Customers with highest spending
print("Highest Spending Customers: ")
q9 = "SELECT Customer_ID, SUM(Total_Amount) AS 'Total' FROM sales GROUP BY Customer_ID ORDER BY Total DESC"
r9 = pd.read_sql_query(q9, conn)
print(r9, "\n")

# Popular Product Categories among Age Groups
print("Popular Categories amongst Age Groups: ")
q10 = "SELECT Product_Category AS 'Category', COUNT(Product_Category) AS 'Count', CASE WHEN Age BETWEEN 18 AND 25 THEN '18-25' WHEN Age BETWEEN 26 AND 35 THEN '26-35' WHEN Age BETWEEN 36 AND 45 THEN '36-45' WHEN Age BETWEEN 46 AND 55 THEN '46-55' ELSE '55+' END AS 'Age_Group' FROM sales GROUP BY Age_Group, Category ORDER BY Age_Group, Count DESC"
r10 = pd.read_sql_query(q10, conn)
print(r10, "\n")

r10.pivot(
    index="Age_Group",
    columns="Category",
    values="Count"
).plot(kind="bar")

plt.title("Most Popular Product Category by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=0)
plt.legend(title="Product Category")
plt.show()
