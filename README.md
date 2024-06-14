### Usage

1. Pre-requisite: Install Docker
2. `docker compose up`
3. Go to `localhost:8080`

### Program assumption

Input file is expected to follow NEM12 specification. Invalid file is not handled and will throw error.

### Security

1. Generating SQL comes with risk of SQL injection if it's not carefully designed. For this case I'm using [PyPika](https://github.com/kayak/pypika). However due to the processing load that comes with sanitizing, this library is significantly slower than generating string. So, for demo purposes I enable an option to turn off sanitizing.
2. For grading convenience, docker compose configuration is currently hardcoded inside docker-compose.yml instead of secured as env variable.
3. JWT security can be added to ensure that user only can access their own file.

### Performance optimisation

As per the problem statement, this software can handle CSV file up to 1 GB. It is expected that the insert statement generated will be larger than 1GB. To avoid storing all the results in the memory resulting in Out Of Memory, the CSV file is processed in batches, with output incrementally written to the disk for each processed chunk.

### Making the service production grade

There are a few choke points that we can identify and improve on from here to create a production grade software

1. Currently the uploaded document is store in file. As this service scale we can use object store such as Amazon S3
2. To prevent files from getting bigger and bigger, have a mechanism to periodically clear the object store. This can be based on the SLA with the users (for example the generated file will be available for one day)
3. sql_generator service scaling: As the SQL generator can take quite some time as the file size is getting bigger. We can create a queue to store all sql_generator job. sql_generator worker can take the job from the queue and asynchronously perform the task and update a status in a cache. User can check the task status by polling to determine when the file is ready for download.
