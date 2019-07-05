# Scraper cars
#### Requirement

    docker
    docker-compose

#### Run
In terminal

    ➜ sudo docker-compose up -d

#### Stop

    ➜ sudo docker-compose down

#### Restart

    ➜ sudo docker-compose restart

#### Check logs

     ➜ sudo docker-compose logs -f
     
### End Point

http://localhost:5000/ - main page;
http://localhost:5000/api/scrap_sites - clear database and re-scrape www.nydailynews.com