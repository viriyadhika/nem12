### Usage

1. Pre-requisite: Install Docker
2. `docker compose up`
3. Go to `localhost:8080`

Demo video: https://youtu.be/8X97DAE1tsA

The web app has 4 capabilities:

1. If you need a sample NEM12 file, format, generate n numbers of unique nmi
2. Upload the generated file or user provided file to the Flask server
3. Get the INSERT statement as a result as a txt file
4. Execute the statement to actually insert it to Postgresql inside the docker container

### Program assumption

Input file is expected to follow NEM12 specification. Invalid file is not handled and will throw error.

When there is a duplicate NMI, it will ignore the duplicated record and log a warning and proceed with the rest . This is why instead of generating one insert statement with all the values, one insert statement is generated for each DB row.

### Security

1. Generating SQL comes with risk of SQL injection if it's not carefully designed. For this case I'm using [PyPika](https://github.com/kayak/pypika). However due to the processing load that comes with sanitizing, this library is significantly slower than generating string. So, for demo purposes I enable an option to turn off sanitizing.
2. For grading convenience, docker compose configuration is currently hardcoded inside docker-compose.yml instead of secured as env variable inside CI/CD pipeline.
3. JWT security can be added to ensure that user only can access their own file.
4. A webserver such as nginx in the web layer can be used as reverse proxy and provide HTTPS connection that's more secure

### Performance optimisation

As per the problem statement, this software can handle CSV file up to 1 GB. It is expected that the insert statement generated will be larger than 1GB. To avoid storing all the results in the memory resulting in Out Of Memory, the CSV file is processed in batches, with output incrementally written to the disk for each processed chunk.

### Basic testing

1. Go to backend folder
   `cd backend`
2. Create venv
   `python3 -m venv .venv`
3. Activate python venv
   `source .venv/bin/activate`
4. Install the package
   `pip install -r requirements.txt`
5. Run Pytest
   `pytest`

### Making the service production grade

There are a few choke points that we can identify and improve on from here to create a production grade software

1. Currently the uploaded document is store in file. As this service scale we can use object store such as AWS S3
2. To prevent files from getting bigger and bigger, have a mechanism to periodically clear the object store. This can be based on the SLA with the users (for example the generated file will be available for one day)
3. sql_generator service scaling: As the SQL generator can take quite some time as the file size is getting bigger. We can create a queue to store all sql_generator job. sql_generator worker can take the job from the queue and asynchronously perform the task and update a status in a cache. User can check the task status by polling to determine when the file is ready for download. In order to do this, it might be also a good idea to separate the services into multiple containers instead of putting them inside one docker container as the current setup.
4. Currently the logs are sent to stdout because we doesn't have logging service. In production scenario, we can push it to Elastic Search and view it through Kibana for monitoring.
5. Add a more comprehensive unit test

### Answer to the questions

1. What does your repository do?

   Under section "Usage"

2. What are the advantages of the technologies you used for the project?

- React: There is a built in state management compared to vanilla javascript.
- Python: There is a native way of opening and parsing CSV.
- PyPika is used to generate inserts query to prevent SQL injection which is possible with simple string concatenation. As a rule of thumb we try to avoid doing our own SQL sanitation logic.
- Flask is used as a very simple webserver wrapper.
- Docker enable me to containerize this application to be run anywhere for the task assessment.
- Docker compose enable me to run multiple docker containers required for this application.

3. How is the code designed and structured? The code is designed based on the components, the main backend components are:

- Flask Webserver
- SQL Generator
- DB integration
- File / storage utils.

  SQL Generator is further subdivided into
- Generate SQL
- Parser
- Mock

  The code flow is as follows.
- Trigger Flask server
- File storage utils is invoked to store user input
- SQL Generator is triggered
- Inside SQL Generator, Parser submodule parse into a dataclass
- Generate SQL submodule then will transform the dataclass into SQL query
- The SQL will be written into a file in batches to limit memory peak usage
- Upon request the result file can be sent back through Flask webserver back to Frontend

  Each of them are independent component that can be swapped without affecting other components. For example,
- Changing storage utils to S3 will require change in File / storage utils and probably a part of Flask Webserver without affecting any other places.
- Changing DB from postgres to MySQL will only affect the DB integration and maybe a minor part of SQL generator so that it's compatible with MySQL but it will not affect the CSV parsing part.
- If the format of NEM12 change, only parser module need to be changed. If there is another file format that needs to be transformed into consumption SQL, we can create multiple parser to create the same dataclass. Generate SQL submodule will not have to change.

4. How does the design help to make the codebase readable and maintainable for other engineers?

   By separating the code into components, other engineers are able to see the flow in the code execution. Python typing with mypy and Typescript is also used to provide typecheck for other engineers.

5. Discuss any design patterns, coding conventions, or documentation practices you implemented to enhance readability and maintainability.

   Generally in Python and Typescript I prefer a functional programming way as I find it easier to follow. However, in this scenario, I use a class / object oriented parser. The reason being that the parser is stateful. In this case, the nmi code of a 300 record is dependent on the last 200 record encountered. Having an object to store enable us to keep the main logic conscise

```python
parser = Parser()
for row in file_reader:
    # Main logic
    parser.parse_row(row)
```

6. What would you do better next time?

   The batching logic to improve performance can be written in a more standardized way. As more and more files get parsed, there might be a few common logics that can be used instead of manually counting the numbers of rows to decide batching.

7. Reflect on areas where you see room for improvement and describe how you would approach them differently in future projects.

   For this project I initially planned to create just a CLI for the user. However after trying the CLI myself I find it not very user friendly. Changing the interface to a web based interface require an extend of code redesign as now I need to implement a file management web server. It would be nice to think of the form factor of the product deeply beforehand.

8. What other ways could you have done this project?

   See under "Making the service production grade"

9. Explore alternative approaches or technologies that you considered during the development of the project.

- I quickly choose Python for the programming language because it enables me to prototype quickly for this kind of data oriented project
- I initially explored ORM library such as SQL Alchemy for the parsing of SQL but end up abandoning it because it has a more awkward API to output the SQL. The more common use case of ORM is to execute the transaction.
- I also explored pandas to parse the CSV input better but it is more challenging to parse NEM12 data as each row has different length which is different from the concept of pandas dataframe.
- To ensure that the batching helps in memory limit, I use tracemalloc to check the peak memory usage during parsing of SQL.
