# REST CRUD API with Dynamic Formatting — Reflection

Coming into this assignment, I already had some experience working with Flask from the previous module, but this project took things further. Instead of simply returning JSON, I built an API that could retrieve, create, update, and delete book records. I started with the professor's example, added *Things Fall Apart* by Chinua Achebe, and changed the endpoints from `/books` to `/goodbooks`.

What I found interesting was how changing data through the API affected what appeared on the webpage. When I updated *In Cold Blood* from a 4.8 rating to 3.5, the conditional formatting meant its row would no longer be highlighted green. It helped me understand how the frontend and backend communicate without manually changing the HTML.

Testing the endpoints also helped me better understand HTTP methods and response codes. Before this assignment, I understood what GET and POST meant conceptually, but actually using POST, PUT, and DELETE made their purposes clearer. I'm interested in exploring how this would work with a database instead of temporary data stored in memory.