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



-- Departments
INSERT INTO departments (department_id, department_name) VALUES
(1, 'IT'),
(2, 'HR'),
(3, 'Finance'),
(4, 'Operations');



-- Employees
INSERT INTO employees (employee_id, employee_name, department_id, email) VALUES
(101, 'Arun Kumar', 1, 'arun@company.com'),
(102, 'Priya Sharma', 1, 'priya@company.com'),
(103, 'Rahul Verma', 2, 'rahul@company.com'),
(104, 'Sneha Iyer', 3, 'sneha@company.com'),
(105, 'Vikram Singh', 4, 'vikram@company.com');



-- Assets
INSERT INTO assets (
    asset_id,
    asset_name,
    asset_type,
    purchase_cost,
    purchase_date,
    status
) VALUES
(201, 'Dell Latitude 5420', 'Laptop', 85000, '2024-01-15', 'Assigned'),

(202, 'HP ProBook 450', 'Laptop', 72000, '2024-02-10', 'Assigned'),

(203, 'iPhone 14', 'Mobile', 65000, '2024-03-05', 'Available'),

(204, 'Samsung Monitor 27"', 'Monitor', 18000, '2024-01-20', 'Assigned'),

(205, 'MacBook Pro M2', 'Laptop', 165000, '2024-04-12', 'Maintenance'),

(206, 'Lenovo ThinkPad', 'Laptop', 92000, '2024-02-22', 'Assigned'),

(207, 'Canon Printer', 'Printer', 25000, '2023-12-01', 'Available'),

(208, 'iPad Air', 'Tablet', 58000, '2024-03-18', 'Assigned');



-- Asset Assignments
INSERT INTO asset_assignments (
    assignment_id,
    asset_id,
    employee_id,
    assigned_date,
    return_date
) VALUES

(301, 201, 101, '2025-01-10', NULL),

(302, 202, 102, '2025-02-15', NULL),

(303, 204, 101, '2025-03-01', NULL),

(304, 206, 104, '2025-01-25', NULL),

(305, 208, 103, '2025-02-18', NULL),

(306, 203, 105, '2024-01-10', '2024-05-20'),

(307, 207, 105, '2024-02-12', '2024-03-15');





-- Maintenance Requests
INSERT INTO maintenance_requests (
    request_id,
    asset_id,
    issue_description,
    maintenance_date,
    cost,
    status
) VALUES

(401, 205, 'Battery replacement issue', '2025-03-15', 12000, 'Pending'),

(402, 201, 'Keyboard malfunction', '2025-02-10', 2500, 'Completed'),

(403, 204, 'Display flickering', '2025-04-05', 3500, 'Pending'),

(404, 207, 'Paper jam issue', '2025-01-12', 1500, 'Completed');