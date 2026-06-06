# yapa
Yet Another Productivity App with no paywall whatsoever and open source code. 

## 🛠️ Environment Configuration

Before running the application, you need to set up your local environment 
variables. The project includes a `.env.example` file populated with default 
configurations and database puns to get you started immediately.

### Create your local .env file
Duplicate the template file and rename it to `.env` in the root directory. 
You can do this quickly by running one of the following terminal commands:

**Linux / macOS:**
```bash
cp .env.example .env
```

**windows:**

Using command Prompt:
```dos
copy .env.example .env
```
Using Powershell

```Powershell
Copy-Item .env.example .env
```
**Default credentials work but it is recomended to modify them!**

## 🛠️ Start the application

**The app will run on the following address: http://localhost:8000**

### First time start

```bash
docker compose up build
```

### Afterwards

```bash
docker compose up
```