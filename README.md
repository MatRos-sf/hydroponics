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
### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/MatRos-sf/hydroponics
   ```
2. Create a virtual environment:
   ```sh
   python3 -m venv venv
   ```
   and active them.
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Build the `.env` file using the provided template in the `sample_env` file.

5. Execute the `migration` command:
    ```sh
    python3 manage.py migrate
    ```
6. And run the server:
    ```sh
    python3 manage.py runserver
    ```




<!-- CONTACT -->
## Contact

Mateusz Rosenkranz - mateuszrosenkranz@gmail.com


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django]: https://img.shields.io/badge/Django-5.0.3-092E20?style=for-the-badge&logo=django
[Django-url]: https://www.djangoproject.com/
[Python]: https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Requests]: https://img.shields.io/badge/Requests-2.26.0-008080?style=for-the-badge&logo=requests
[Requests-url]: https://docs.python-requests.org/en/latest/
[Django_Rest_Framework]: https://img.shields.io/badge/Django%20Rest%20Framework-3.14.0-03282C?style=for-the-badge&logo=django
[Django_Rest_Framework-url]: https://www.django-rest-framework.org/
[Factory_Boy]: https://img.shields.io/badge/Factory%20Boy-3.2.0-FF69B4?style=for-the-badge&logo=python
[Factory_Boy-url]: https://factoryboy.readthedocs.io/en/stable/
[Parameterized]: https://img.shields.io/badge/Parameterized-0.8.1-00CED1?style=for-the-badge&logo=python
[Parameterized-url]: https://parameterizedtestcase.readthedocs.io/en/latest/
