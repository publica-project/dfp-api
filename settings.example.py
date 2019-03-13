import os

GOOGLEADS_YAML_FILE = os.getenv('GOOGLEADS_CONFIG', 'googleads.yaml')

#########################################################################
# DFP SETTINGS
#########################################################################

# A string describing the order
# Line items will also use this name
GA_ORDER_NAME = 'Publica Prebid'

# If an existing order is found:
# if True, use the existing order,
# if False, will fail.
GA_USE_EXISTING_ORDER = True

# The name of the advertiser to use for the created order.
# run "python -m src.advertisers" to see the list of advertisers
GA_ADVERTISER_NAME = 'Prebid'

# The email of the Google Ads user who will be the trafficker for the created order.
# run "python -m src.users" to see the list of users
GA_USER_EMAIL = 'email@email.com'

# The targeted ad unit used by the created line items.
# run "python -m src.ad_units" to see the list of active ad units.
GA_AD_UNIT_ID = 0 

# Id of the creative or creative set to associate with the created line items
# Find this in your DFP account.
GA_CREATIVE_ID = 0
GA_CREATIVE_IS_SET = False

# Price buckets. This should match your Prebid settings for the partner. See:
# http://prebid.org/dev-docs/publisher-api-reference.html#setConfig-Price-Granularity
# 'auto' is set as:
#   PREBID_PRICE_BUCKETS = [{
#     'min' : 0,
#     'max' : 5,
#     'increment': 0.05,
#     'precision': 2,
#   }, {
#     'min' : 5,
#     'max' : 10,
#     'increment': 0.1,
#     'precision': 2,
#   }, {
#     'min' : 10,
#     'max' : 20,
#     'increment': 0.5,
#     'precision': 2,
#   }]
PREBID_PRICE_BUCKETS = 'auto'
