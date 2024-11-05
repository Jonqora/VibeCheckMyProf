# Grafana Cloud Setup

You should have completed the `DATABASE.md` setup steps and and have the RDS database running on your account. You should have recently re-run `terraform apply` as well, on a branch that has the Grafana IPs added.

1. Visit [Grafana](https://vcmp.grafana.net/)
   - Expand Connections in the left side hamburger menu
   - Select Add New Connection
   - Choose MySQL data source (NOT MySQL integration)
   - Choose Add new data source

2. Enter settings information
   - Name your Grafana MySQL connection (remember for later)
   - Find what to enter for Host, Database, User and Password from the fields in `infra/config.env`: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD 
   - Connect data 

3. Create a dashboard (for example)
   - Search from the top bar "new dashboard"
   - Add visualization
   - Find the data source you created and named in the previous steps
   - Where you see Builder | Code, select Code
   - Enter your query in the field. For example:
```
SELECT *
FROM ratings
WHERE quality = 5
```