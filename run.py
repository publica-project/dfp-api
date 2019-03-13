import time
import numbers
import settings
from src import utils
from src import orders
from src import creatives
from src import line_items
from src import advertisers
from src import users
from src import licas

def check_settings():
  if settings.GA_ORDER_NAME is None:
    utils.logError('settings.GA_ORDER_NAME cannot be None.')
    return False

  if settings.GA_ADVERTISER_NAME is None:
    utils.logError('settings.GA_ADVERTISER_NAME cannot be None.')
    return False

  if settings.GA_USER_EMAIL is None:
    utils.logError('settings.GA_USER_EMAIL cannot be None.')
    return False
  
  if settings.GA_CREATIVE_ID is None:
    utils.logError('settings.GA_CREATIVE_ID cannot be None.')
    return False

  if not settings.GA_USE_EXISTING_ORDER:
    order = orders.get(settings.GA_ORDER_NAME)
    if order is not None:
      utils.logError('Order with name "%s" already exists. You must use a different name.' % order['name'])
      return False

  advertiser = advertisers.get(settings.GA_ADVERTISER_NAME)
  if (advertiser is None):
    utils.logError('Advertiser with id "%s" does not exists.' % settings.GA_ADVERTISER_NAME)

  user = users.get(settings.GA_USER_EMAIL)
  if (user is None):
    utils.logError('Advertiser with email "%s" does not exists.' % settings.GA_USER_EMAIL)

  creative = creatives.get(settings.GA_CREATIVE_ID)
  if (creative is None):
    utils.logError('Creative with id "%s" does not exists. You must specify an existing creative id.' % settings.GA_CREATIVE_ID)

  # check data structure of PREBID_PRICE_BUCKETS
  if settings.PREBID_PRICE_BUCKETS == 'auto':
    settings.PREBID_PRICE_BUCKETS = [{
      'min' : 0,
      'max' : 5,
      'increment': 0.05,
      'precision': 2,
    }, {
      'min' : 5,
      'max' : 10,
      'increment': 0.1,
      'precision': 2,
    }, {
      'min' : 10,
      'max' : 20,
      'increment': 0.5,
      'precision': 2,
    }]
  else:
    for bucket in settings.PREBID_PRICE_BUCKETS:
      if 'min' not in bucket or 'max' not in bucket or 'increment' not in bucket:
        utils.logError('settings.PREBID_PRICE_BUCKETS invalid format. Requires "min", "max", and "increment"')
        return False
      if 'precision' not in bucket:
        bucket['precision'] = 2
      for name in ['min', 'max', 'increment', 'precision']:
        if not isinstance(bucket[name], numbers.Number):
          utils.logError('"%s" must be a number in settings.PREBID_PRICE_BUCKETS' % name)
          return False

  return True

def main():
  print('This script will do a few things:')
  print('  1) Check settings')
  print('  2) Create Order')
  print('  3) Create Line Items')
  print('    3.1) Create Line Item Creative Associations')
  print('    3.2) Link Line Items and the Creative Association together')

  print('Checking settings...')
  if not check_settings():
    return

  print('Settings look good.')

  print('Creating order with name "%s"...' % settings.GA_ORDER_NAME)
  order = None
  if settings.GA_USE_EXISTING_ORDER:
    order = orders.get(settings.GA_ORDER_NAME)
  
  if order is None:
    order = orders.create(settings.GA_ORDER_NAME)
    if order is None:
      utils.logError('Failed to create order.')
      return
    print('Created order named "%s" with ID "%s"' % (order['name'], order['id']))    
  else:
    print('Using existing order named "%s" with ID "%s"' % (order['name'], order['id']))

  print('Creating line items and associations...')
  config = line_items.generate_configs()
  count = 1
  for c in config:
    line_item = line_items.create(order['id'], c)
    print('(%s/%s) Created line item with ID "%s"' % (count, len(config), line_item['id']))
    time.sleep(1)
    lica = licas.create(line_item['id'], settings.GA_CREATIVE_ID)
    print('(%s/%s) Created association between line item "%s" and creative set "%s"' %(count, len(config), lica['lineItemId'], settings.GA_CREATIVE_ID))
    count += 1
  
  print('Line items and association(s) created. Please check your DFP account to see the changes.')
  print('\nDone.')

if __name__ == '__main__':
  main()
  