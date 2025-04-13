from gapSolutions_client.config import set_base_url
from gapSolutions_client.folder.folder import folder_list
from gapSolutions_client.constants import base_token

set_base_url("https://testapp.gapsolutions.dk/api")


response = folder_list(auth_token=base_token, query_params={"lang": "en"})
print("response", response)