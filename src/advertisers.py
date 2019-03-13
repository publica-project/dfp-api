import googleads
import client

ga_client = client.get_client()
company_service = ga_client.GetService('CompanyService', version='v201811')

def get(name):
  if name is None:
    return None
    
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('type = :type')
               .WithBindVariable('type', 'ADVERTISER')
               .Where('name = :name')
               .WithBindVariable('name', name))

  response = company_service.getCompaniesByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for advertiser in response['results']:
      return advertiser
  
  return None

def printOut():
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('type = :type')
               .WithBindVariable('type', 'ADVERTISER'))
  
  response = company_service.getCompaniesByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    print('Found %s Advertiser(s):' % len(response['results']))
    for advertiser in response['results']:
      print('  "%s" with ID "%s".' % (advertiser['name'], advertiser['id']))
  
  else:
    print('No Advertisers found.')

  print('')

if __name__ == '__main__':
  printOut()