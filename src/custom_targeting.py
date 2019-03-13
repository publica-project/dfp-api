import googleads
import client

ga_client = client.get_client()
custom_targeting_service = ga_client.GetService('CustomTargetingService', version='v201811')

def get(key_name, value):
  key = create_key(key_name)
  c_value = create_value(key['id'], value)
  return {
    'key': key,
    'value': c_value
  }

def get_key(name):
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('name = :name')
               .WithBindVariable('name', name))

  response = custom_targeting_service.getCustomTargetingKeysByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for key in response['results']:
      return key
  
  return None

def create_key(name):
  key = get_key(name)
  if key is not None:
    return key

  key_to_create = {
    'name': name,
    'type': 'FREEFORM',
  }

  created_keys = custom_targeting_service.createCustomTargetingKeys([key_to_create])
  for key in created_keys:
    return key
  
  return None

def get_value(key_id, value):
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('customTargetingKeyId = :key_id and name = :value and status = :status')
               .WithBindVariable('key_id', key_id)
               .WithBindVariable('value', value)
               .WithBindVariable('status', 'ACTIVE'))
  
  response = custom_targeting_service.getCustomTargetingValuesByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for value in response['results']:
      return value

  return None

def create_value(key_id, value):
  g_value = get_value(key_id, value)
  if g_value is not None:
    return g_value

  value_to_create = {
    'customTargetingKeyId': key_id,
    'name': value
  }
  
  created_values = custom_targeting_service.createCustomTargetingValues([value_to_create])
  for value in created_values:
    return value

  return None
