# profilechange - Automate profile id change for multiple datasources # 

Change profile ids for all Google Analytics Datasources on a particular client via the Klipfolio API

## Running the script ##

- Extract the files from the profilechange.zip 
- Edit the config.json 

config.json
``` javascript
{
	"client_id": "04689d15b8b9e18f8872de41d8d34f3b", //The Public ID of the client that you would like to effect
	"profile_id": "01234567", //Your Google Analytics profile id that starts with "ga:"
	"username": "example@klipfolio.com", //Your Klipfolio Username
	"verbose": "y", //set verbose to "y" to allow for detailed reporting and refreshing of datasources 
}
```

- Double click profile_change.exe
- Enter your password, and let the script run
