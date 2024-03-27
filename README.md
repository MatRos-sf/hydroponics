<a name="readme-top"></a>


<div align="center">
<h1 align="center">Hydroponics</h1>

  <p align="center">
    <a href="https://github.com/MatRos-sf/hydroponics/issues">Report Bug</a>
    ·
    <a href="https://github.com/MatRos-sf/hydroponics/issues">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project
This project serves as a simple Hydroponic Systems Manager. It was initially developed as part of an interview exercise for Luna Company.
Its main goals were to:
* Create models for hydroponic systems
* Set up basic operations for managing hydroponic systems (CRUD)
* Allow submitting measurements from sensors
* Provide functionality for reading information about systems and measurements.
* Implement user authentication and permissions.



### Built With

* [![Django][Django]][Django-url]
* [![Python][Python]][Python-url]
* [![Django_Rest_Framework][Django_Rest_Framework]][Django_Rest_Framework-url]


<!-- GETTING STARTED -->
## Getting Started
You can install this project in two different ways: using venv or using poetry.
### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/MatRos-sf/hydroponics .
   ```
2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Build the `.env` file using the provided template in the `sample_env` file.
   ```text
   SECRET_KEY=...
   DEBUG=TRUE
   ALLOWED_HOSTS=*

   #DATA
   DB_NAME=...
   DB_USER=...
   DB_PASSWORD=...
   DB_HOST=...
   DB_PORT=...
   ```
5. Run the `migration` command:
    ```sh
    python3 manage.py migrate
    ```
6. And run the server:
    ```sh
    python3 manage.py runserver
    ```
### Installation with poetry
1. Clone the repository:
   ```sh
   git clone https://github.com/MatRos-sf/hydroponics .
   ```
2. Install:
   ```sh
   poetry install
   ```

3. Build the `.env` file using the provided template in the `sample_env` file.

4. Execute the `migration` command:
    ```sh
    poetry run python3 manage.py migrate
    ```
5. Start the server:
    ```sh
    poetry run python3 manage.py runserver
    ```

## API documentation
To access the app documentation, visit ```http://127.0.0.1:8000/api/swagger/``` or refer to the provided screenshot:
![Zrzut ekranu z 2024-03-27 22-48-08](https://github.com/MatRos-sf/hydroponics/assets/59665130/e2e012c8-8e52-4fd8-a824-61dbebc6e3c4)

## Scripts and tests
<p>I've created a script to assist you in generating sample models, which you can use to test the application.</p>
Additionally, there are 65 tests that cover 99% of my code. If you'd like to test this application, use:

```shell
  coverage run manage.py test
  coverage html
```




<!-- CONTACT -->
## Contact

#### Mateusz Rosenkranz
* mateuszrosenkranz@gmail.com
* www.linkedin.com/in/mat-ros


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django]: https://img.shields.io/badge/Django-5.0.3-092E20?style=for-the-badge&logo=django
[Django-url]: https://www.djangoproject.com/
[Python]: https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Requests]: https://img.shields.io/badge/Requests-2.26.0-008080?style=for-the-badge&logo=requests
[Requests-url]: https://docs.python-requests.org/en/latest/
[Django_Rest_Framework]: https://img.shields.io/badge/Django%20Rest%20Framework-3.15.1-03282C?style=for-the-badge&logo=django
[Django_Rest_Framework-url]: https://www.django-rest-framework.org/
[Factory_Boy]: https://img.shields.io/badge/Factory%20Boy-3.2.0-FF69B4?style=for-the-badge&logo=python
[Factory_Boy-url]: https://factoryboy.readthedocs.io/en/stable/
[Parameterized]: https://img.shields.io/badge/Parameterized-0.8.1-00CED1?style=for-the-badge&logo=python
[Parameterized-url]: https://parameterizedtestcase.readthedocs.io/en/latest/
