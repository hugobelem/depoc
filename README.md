# DEPOC 

A comprehensive management system built by a business owner, tailored for small Brazilian businesses.

This project took shape in response to a specific need in my last brick-and-mortar store. After closing the business, I continued developing and refining the system.

## Modules

The system covers the full business workflow—from purchasing to sales and issuing Brazil’s electronic tax invoice (NFe). Proposed modules under development:

* **Inventory Management** ✅

  * Track stock movements: inbound, outbound

* **Contacts Management** ✅

  * Categorize contacts: customers, suppliers

* **User Management with RBAC** ✅

  * Role-based access control for members

* **Billing** ✅

  * Manage accounts payable and receivable
  * Auto-update overdue status
  * Support installments (weekly/monthly)

* **Product Management** ✅

  * Track cost and price history
  * Support hierarchical categorization

* **Finance** ✅

  * Monitor cash inflows/outflows
  * Categorize income/expenses
  * Maintain running balances

* **Business Fiscal Data** ✅

* **Sales** ⚒️

* **Brazilian Tax Invoice (Nota Fiscal)** ⚒️

---

## Stack

* **Backend**

  * Python + Django

* **Infrastructure**

  * **AWS**
    * EC2 (hosting)
    * RDS (PostgreSQL)
    * Route 53 (DNS)
  * **Nginx** as reverse proxy
  * **Celery** for asynchronous tasks
  * **RabbitMQ** for monitoring payment due dates
  * **GitHub Actions** for CI/CD

---
