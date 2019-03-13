DFP API
===================================

## Python

- This script uses [Python](https://www.python.org/), so you'll need to install if you don't already have it installed.

## Setup

1. Run the python setup
    1. To automatically prepare the terminal shell, run `direnv allow`. See [https://direnv.net](https://direnv.net) for more info on how it works.
    2. If not using direnv, run `./setup.sh`.
2. Run `python -m src.users` to check whether environment is setup and credentials are valid.
    ```sh
    $ python get_all_users.py
    ```

## Config: googleads.yaml

By default, the client will look at the present working directory to find `googleads.yaml`. This can be overridden by setting the a path by `GOOGLEADS_CONFIG=/dir/to/config/googleads.yaml`.

```sh
GOOGLEADS_CONFIG=/dir/to/config/googleads.yaml python -m src.users
```

## Enable API Access and Add Service Account
- https://www.google.com/dfp/
- Admin > Global Settings > Add a Service Account User
- Use the email of the Service Account created in the previous section

## Create Service Account
- https://console.developers.google.com/apis/credentials
- Create Project (if needed)
- Create credentials > Service account key
- Create Service account (if needed)
- Key type: JSON
- Create
- Save the downloaded file to `key.json` in the root directory

## Setup env

### googleads.yaml
- Copy and rename `googleads.example.yaml` to `googleads.yaml`
- Open and edit the `googleads.yaml` file
- Change `aplication_name` and `network_code`

```yml
ad_manager:
  application_name: ANYTHING
  network_code: CAN_BE_FOUND_IN_THE_URL
  path_to_private_key_file: ./key.json
```
### setup.py
- Copy and rename `setup.example.py` to `setup.py`
- Open and edit the `setup.py` file
- Change the values as needed

### src/line_items.py
- The properties and values for line item creation has not been moved to a separate config yet so for now, you need to check the `src/line_items.py` file.

## Running the scoript
- After everything is setup, run the script with:

```
python -m run
```