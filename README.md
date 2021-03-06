# Funky Fresh Food Finder
The purpose of this application is to enable a user to be able generate a random restaurant suggestion based off their selected criteria. The user is able to enter different information such as location, food type, category, radius, and price point to pin down certain restraints for the type of restaurants that may be returned. After the user selects their critera, one restaurant will be returned to the user with information such as the name, address, price point, and website (if applicable). The user has an option to save their generated result and reroll for a new random restaurant. They can save as many as they want and later delete a specific saved restaurant or clear all the saved results.

## Installation
Here is what needs to be installed to run the program
* [python3](https://www.python.org/downloads/)
* [Flask](https://pypi.org/project/Flask/)
* [Jinja2](https://pypi.org/project/Jinja2/)
* [requests](https://pypi.org/project/requests/)

Assuming python3 and [pip](https://pip.pypa.io/en/stable/installation/) is installed, you can run the shell script to install the dependencies needed for the project.

```bash
./downloads.sh
```

May need to change file permissions to run the shell script as done below.

```bash
chmod +x downloads.sh
```

## Run
To run the program put in the following command in the terminal.

```bash
python3 main.py
```

This will allow the user to see and interact with the program [here](http://127.0.0.1:5000/).