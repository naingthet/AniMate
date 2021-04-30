<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/naingthet">
    <img src="webapp/app/static/assets/img/logo.png" alt="Logo" width="500" height="70">
  </a>

  <h3 align="center">Anime Recommendation System</h3>

  <p align="center">
    A collaborative filtering recommendation system for anime lovers!
  </p>
  <p align="center"> This repository is no longer maintained.</p> 
</p>





<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][animate-homepage]](webapp/app/static/assets/img/animate-homepage.png)

AniMate is a collaborative filtering recommendation system built for anime loves to find new content. AniMate is powered by a singular value decomposition (SVD) algorithm, which uses data from millions of anime ratings to provide users with recommendations.


### Built With


* [Python](https://python.org)
* [Flask](https://palletsprojects.com/p/flask/)
* [Bootstrap](https://getbootstrap.com)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Elasticsearch](https://www.elastic.co/)




## Features

- Secure user accounts and profiles
- Ability to search and rate animes
- Full-text search capabilities powered by Elasticsearch
[![Product Name Screen Shot][search]](webapp/app/static/assets/img/search.png)
<br><br>

- Personalized anime recommendations powered by collaborative filtering
[![Product Name Screen Shot][recommendations]](webapp/app/static/assets/img/recommendations.png)
<br><br>

- Personalized dashboard to track user ratings and find most popular animes
[![Product Name Screen Shot][dashboard]](webapp/app/static/assets/img/dashboard.png)
<br><br>



## Project Roadmap

- [x] **Authentication**

  - [x] Register
  - [x] Login
  - [x] Forgot password
  - [x] Reset password
  - [x] Hash-protected passwords

- [x] **Support**

  - [x] Password support
  - [x] Contact administrator
  - [x] Error logging

- [x] **Database**

  - [x] User information
  - [x] Anime information
  - [x] User rating data

- [x] **Search**

  - [x] Search animes by name
  - [x] Rate animes 
  - [x] View anime ratings
  - [x] Change anime ratings
  - [x] Anime information pages


- [x] **Recommendations**

  - [x] Recommend animes based on user ratings
  - [x] Timeline
  - [x] Company Overview
  - [x] Responsibilities

- [x] **Dashboard**

  - [x] User statistics
  - [x] Top rated animes
  - [x] Most popular animes
  - [x] User's favorite animes
  - [x] User's most recent ratings

- [ ] **Background Processes**
  - [ ] Train models in background after user rates new animes

- [ ] **Deployment**

  - [ ] Migrate SQLAlchemy databases to PostgreSQL
  - [ ] Deploy application to Heroku


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.





[animate-homepage]: webapp/app/static/assets/img/animate-homepage.png
[dashboard]: webapp/app/static/assets/img/dashboard.png
[search]: webapp/app/static/assets/img/search.png
[recommendations]: webapp/app/static/assets/img/recommendations.png
