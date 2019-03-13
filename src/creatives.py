import googleads
import client
import settings

ga_client = client.get_client()
creative_service = ga_client.GetService('CreativeService', version='v201811')
creative_set_service = ga_client.GetService('CreativeSetService', version='v201811')

def get(id):
  if id is None:
    return None

  service_name = 'CreativeService'
  if settings.GA_CREATIVE_IS_SET:
    service_name = 'CreativeSetService'
  
  service = ga_client.GetService(service_name, version='v201811')

  statement = (googleads.ad_manager.StatementBuilder()
               .Where('ID = :id')
               .WithBindVariable('id', id))
  if settings.GA_CREATIVE_IS_SET:
    response = service.getCreativeSetsByStatement(statement.ToStatement())
  else:
    response = service.getCreativesByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for creative in response['results']:
      return creative
  
  return None
