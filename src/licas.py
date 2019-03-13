import math
import googleads
import client
import settings
import custom_targeting

ga_client = client.get_client()
lica_service = ga_client.GetService('LineItemCreativeAssociationService', version='v201811')

field_name = 'creativeId'
if settings.GA_CREATIVE_IS_SET:
  field_name = 'creativeSetId'

def get(line_item_id, creative_id):
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('lineItemId = :line_item_id and ' + field_name + ' = :creative_id')
               .WithBindVariable('line_item_id', line_item_id)
               .WithBindVariable('creative_id', creative_id))

  response = lica_service.getLineItemCreativeAssociationsByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for lica in response['results']:
      return lica
  
  return None

def create(line_item_id, creative_id):
  lica = get(line_item_id, creative_id)
  if lica is not None:
    return lica

  lica_to_create = {
    'lineItemId': line_item_id,
    field_name: creative_id,
  }

  created_licas = lica_service.createLineItemCreativeAssociations([lica_to_create])

  for lica in created_licas:
    return lica