<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/unblock_data_viz/scratch/image_files/grafana.png" width="50" height="50" />
</p> 


## Grafana Cloud Setup

The following steps will guide you on how to connect your AWS RDS database to Grafana Cloud. 

You should have completed the `DATABASE.md` setup steps and have the RDS database running on your account. You should have recently re-run `terraform apply` as well, on a branch that has the Grafana IPs added.

1. Visit [Grafana](https://vcmp.grafana.net/)
   - Expand Connections in the left side hamburger menu
   - Select Add New Connection
   - Choose MySQL data source (NOT MySQL integration)
   - Choose Add new data source

2. Enter settings information
   - Name your Grafana MySQL connection (remember for later)
   - Find what to enter for Host, Database Name, User and Password from the fields in `infra/config.env`: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD 
   - Connect data 

3. Create a dashboard (for example)
   - Search from the top bar "new dashboard"
   - Add visualization
   - Find the data source you created and named in the previous steps
   - At the bottom of your screen where you see Builder | Code, select Code
   - At the right side of your screen, you can select the visualization type in the dropdown options
   - Enter your query in the field. For example:
```
SELECT *
FROM ratings
WHERE quality = 5
```