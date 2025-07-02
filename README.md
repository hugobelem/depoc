# DEPOC 

A comprehensive management system built by a business owner, tailored for small Brazilian businesses.

This project took shape in response to a specific need in my last brick-and-mortar store. After closing the business, I continued developing and refining the system.

The system exposes a RESTful interface at the root endpoint https://api.depoc.com.br, serving as the primary access point for client interactions.

## Modules

This API aims to covers the basic business workflow. From purchasing to sales and issuing Brazil’s electronic tax invoice (NFe). Proposed modules under development:

* **User Management with RBAC** ✅

  * Role-based access control

* **Contacts Management** ✅

  * Categorize contacts: customers, suppliers

* **Product Management** ✅

  * Track cost and price history
  * Support hierarchical categorization

* **Inventory Management** ✅

  * Track stock movements: inbound, outbound

* **Billing** ✅

  * Manage accounts payable and receivable
  * Auto-update overdue status
  * Support installments (weekly/monthly)

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
