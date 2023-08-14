# Parser_test

Backend for dino game in telegram

## Prerequisites

Before you start using this project, make sure you have Python installed on your computer. Follow the steps below to install Python based on your operating system:

### Windows

1. Open a web browser and go to the official Python website: https://www.python.org/downloads/windows/
2. Download the latest version of Python for Windows.
3. Run the installer and make sure to check the box that says "Add Python to PATH".
4. Follow the on-screen instructions to complete the installation.
## Installation

1. Сlone the repository to the target folder where the project should be located

```bash
git clone link
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Create .env file with all neccessary variables. It is neccessary to set your own telegram api TOKEN

### Alembic configuration
4. Initialize alembic migrations

```bash
alembic init migrations
```

5. In file alembic.ini update value of variable **sqlalchemy.url** to your url to database
6. In file migrations/env.py update row **target_metadata = None** with:
```bash
from models.models import Base
target_metadata = Base.metadata
```

7. Run
```bash
alembic revision --autogenerate
alembic upgrade head
```

8. Run the app
```bash
uvicorn main:app --reload  
```

9. Run the telegram bot from the telegram directory
```bash
python tg_bot.py
```
 



