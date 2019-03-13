import googleads
import client

ga_client = client.get_client()
inventory_service = ga_client.GetService('InventoryService', version='v201811')

def printOut():
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('status = :status')
               .WithBindVariable('status', 'ACTIVE'))
  
  response = inventory_service.getAdUnitsByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    print('Found %s Ad Unit(s):' % len(response['results']))
    for ad_unit in response['results']:
      print('  "%s" with ID "%s".' % (ad_unit['name'], ad_unit['id']))
  
  else:
    print('No Ad Units found.')

  print('')

if __name__ == '__main__':
  printOut()