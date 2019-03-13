import googleads
import client
import settings
import advertisers
import users

ga_client = client.get_client()
order_service = ga_client.GetService('OrderService', version='v201811')

def get(name):
  if name is None:
    return None

  statement = (googleads.ad_manager.StatementBuilder()
               .Where('name = :name')
               .WithBindVariable('name', name))
  
  response = order_service.getOrdersByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for order in response['results']:
      return order
  
  return None

def create(name):
  advertiser = advertisers.get(settings.GA_ADVERTISER_NAME)
  user = users.get(settings.GA_USER_EMAIL)

  order_to_create = {
    'name': name,
    'advertiserId': advertiser['id'],
    'traffickerId': user['id']
  }

  created_orders = order_service.createOrders([order_to_create])
  for order in created_orders:
    return order

  return None