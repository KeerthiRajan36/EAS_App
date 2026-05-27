-- 1. Find Most Assigned Assets
SELECT 
    a.asset_id,
    a.asset_name,
    COUNT(aa.asset_id) AS assignment_count
FROM assets a
JOIN asset_assignments aa 
    ON a.asset_id = aa.asset_id
GROUP BY a.asset_id, a.asset_name
ORDER BY assignment_count DESC;


-- 2. Employees Holding Multiple Assets
SELECT 
    e.employee_id,
    e.employee_name,
    COUNT(aa.asset_id) AS total_assets
FROM employees e
JOIN asset_assignments aa 
    ON e.employee_id = aa.employee_id
WHERE aa.return_date IS NULL
GROUP BY e.employee_id, e.employee_name
HAVING COUNT(aa.asset_id) > 1;


-- 3. Monthly Maintenance Cost Report
SELECT 
    YEAR(maintenance_date) AS year,
    MONTH(maintenance_date) AS month,
    SUM(cost) AS total_maintenance_cost
FROM maintenance_requests
GROUP BY YEAR(maintenance_date), MONTH(maintenance_date)
ORDER BY year DESC, month DESC;


-- 4. Assets Not Used for Last 6 Months
SELECT 
    a.asset_id,
    a.asset_name,
    MAX(aa.assigned_date) AS last_used_date
FROM assets a
LEFT JOIN asset_assignments aa
    ON a.asset_id = aa.asset_id
GROUP BY a.asset_id, a.asset_name
HAVING MAX(aa.assigned_date) < CURRENT_DATE - INTERVAL 6 MONTH
   OR MAX(aa.assigned_date) IS NULL;


-- 5. Asset Utilization Percentage
SELECT 
    a.asset_id,
    a.asset_name,
    ROUND(
        (
            COUNT(CASE WHEN aa.return_date IS NULL THEN 1 END) * 100.0
        ) / COUNT(aa.asset_id),
        2
    ) AS utilization_percentage
FROM assets a
LEFT JOIN asset_assignments aa
    ON a.asset_id = aa.asset_id
GROUP BY a.asset_id, a.asset_name;


-- 6. Department-wise Asset Allocation Report
SELECT 
    d.department_name,
    COUNT(aa.asset_id) AS total_allocated_assets
FROM departments d
JOIN employees e 
    ON d.department_id = e.department_id
JOIN asset_assignments aa 
    ON e.employee_id = aa.employee_id
WHERE aa.return_date IS NULL
GROUP BY d.department_name
ORDER BY total_allocated_assets DESC;


-- 7. Top 5 Expensive Assets
SELECT 
    asset_id,
    asset_name,
    purchase_cost
FROM assets
ORDER BY purchase_cost DESC
LIMIT 5;


-- 8. Assets Under Maintenance with Pending Requests
SELECT 
    a.asset_id,
    a.asset_name,
    mr.request_id,
    mr.issue_description,
    mr.status
FROM assets a
JOIN maintenance_requests mr
    ON a.asset_id = mr.asset_id
WHERE mr.status = 'Pending';


-- 9. Employee Asset Audit Report Using JOINs
SELECT 
    e.employee_id,
    e.employee_name,
    d.department_name,
    a.asset_name,
    aa.assigned_date,
    aa.return_date
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN asset_assignments aa
    ON e.employee_id = aa.employee_id
JOIN assets a
    ON aa.asset_id = a.asset_id
ORDER BY e.employee_name;


-- 10. Rank Departments by Asset Value Using Window Functions
SELECT 
    d.department_name,
    SUM(a.purchase_cost) AS total_asset_value,
    RANK() OVER (
        ORDER BY SUM(a.purchase_cost) DESC
    ) AS department_rank
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
JOIN asset_assignments aa
    ON e.employee_id = aa.employee_id
JOIN assets a
    ON aa.asset_id = a.asset_id
GROUP BY d.department_name;