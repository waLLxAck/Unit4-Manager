
# Unit4-Manager
A tool that helps you manage all things - Unit4.

## How to use

1. Add your new project settings
This is done in ``new_bookmarks.json``

![2022-06-25 09 48 37 Unit4-Manager – new_bookmarks](https://user-images.githubusercontent.com/15944458/175763257-2b125118-71f5-4d0f-8b66-50a0d75800b2.png)

2. Update your 'Bookmarks' file path. 
Normally this is stored in:
```
C:\\Users\\_YOUR_USER\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks
```

![2022-06-25 10 15 20 Unit4-Manager – settings](https://user-images.githubusercontent.com/15944458/175763264-285dbfab-2059-4ff5-a7a3-00643a1d24e3.png)

3. Run ``main.py``.

![image](https://user-images.githubusercontent.com/15944458/175808713-6b38342d-c44b-48d9-832d-f565d26fbea9.png)

4. Check your bookmarks to confirm results.

![image](https://user-images.githubusercontent.com/15944458/175808825-2895f274-4ea7-4c7d-99ca-e5005162dcf1.png)

## Available tools

### Bookmark manager

Adds project information to your bookmarks. 

It starts by creating a base 'Unit4' folder on the bookmarks tab, if that doesn't exist. It then creates a 'Projects' folder inside. Then inside 'Projects' it creates a folder using the project name that's supplied in ``new_bookmarks.json``. Inside, it proceeds to create the following URLS:

- Swagger API
- Extension Kit - PREV, ACPT, PROD
- ERP Lab - PREV, ACPT, PROD

### Insomnia collection builder

Builds an insomnia JSON file that you can import into your insomnia environment that has all the settings supplied in the ``new_bookmarks.json`` file.

The structure that it follows:

```
{
	"urls": {
		"swagger_api": ""
	},
	"authorization": {
		"erp": {
			"prev": {
				"company_id": "",
				"access_token_url": "",
				"client_id": "",
				"client_secret": ""
			},
			"acpt": {
				"company_id": "",
				"access_token_url": "",
				"client_id": "",
				"client_secret": ""
			},
			"prod": {
				"company_id": "",
				"access_token_url": "",
				"client_id": "",
				"client_secret": ""
			}
		}
	}
}
```

Additionally, it creates a sample GET request with one of the environments' settings so that you can test the credentials straight away.

![image](https://user-images.githubusercontent.com/15944458/175808535-ae6e07dc-5211-4b28-b1f3-a5d8d47a4055.png)


_Note: The GET request is set to ``/v1/objects/attribute-values`` and it has a filter to look for attribute C1 (Cost Center)._
