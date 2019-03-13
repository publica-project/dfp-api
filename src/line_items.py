import math
import googleads
import client
import settings
import custom_targeting

ga_client = client.get_client()
line_item_service = ga_client.GetService('LineItemService', version='v201811')

def generate_configs():
  values = []
  for bucket in settings.PREBID_PRICE_BUCKETS:
    factor = math.pow(10, bucket['precision'])
    formater = '{:.%sf}' % bucket['precision']
    i = bucket['min']
    while i < bucket['max']:
      if i > 0:
        value = round(i * factor) / factor
        values.append(formater.format(value))
      i += bucket['increment']

  values.append(formater.format(settings.PREBID_PRICE_BUCKETS[-1]['max']))

  config = []
  for value in values:
    config.append({
      'name': '%s: Line Item - %s' % (settings.GA_ORDER_NAME, value),
      'value': value
    })
    
  return config

def get(order_id, config):
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('name = :name and orderId = :order_id')
               .WithBindVariable('name', config['name'])
               .WithBindVariable('order_id', order_id))

  response = line_item_service.getLineItemsByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for line_item in response['results']:
      return line_item
  
  return None

def create(order_id, config):
  line_item = get(order_id, config)
  if line_item is not None:
    return line_item

  targeting = custom_targeting.get('hb_pb', config['value'])

  line_item_to_create = {
    'name': config['name'],
    'orderId': order_id,
    'startDateTimeType': 'IMMEDIATELY',
    'unlimitedEndDateTime': True,
    'creativeRotationType': 'EVEN',
    'deliveryRateType': 'FRONTLOADED',
    'roadblockingType': 'ONE_OR_MORE',
    'lineItemType': 'PRICE_PRIORITY',
    'costPerUnit': {
      'currencyCode': 'USD',
      'microAmount': int(float(config['value']) * 1000000)
    },
    'costType': 'CPM',
    'discountType': 'PERCENTAGE',
    'creativePlaceholders': [
      {
        'size': {
          'width': '670',
          'height': '338',
        },
      }
    ],
    'environmentType': 'VIDEO_PLAYER',
    'companionDeliveryOption': 'OPTIONAL',
    'videoMaxDuration': '0',
    'primaryGoal': {
      'goalType': 'NONE',
    },
    'targeting': {
      'inventoryTargeting': {
        'targetedAdUnits': [{
          'adUnitId': settings.GA_AD_UNIT_ID,
        }],
      },
      'customTargeting': {
        'xsi_type': 'CustomCriteriaSet',
        'logicalOperator': 'AND',
        'children': [{
          'xsi_type': 'CustomCriteria',
          'keyId': targeting['key']['id'],
          'valueIds': [targeting['value']['id']],
          'operator': 'IS'
        }]
      },
      'requestPlatformTargeting': {
        'targetedRequestPlatforms': [
          'VIDEO_PLAYER',
        ]
      }
    }
  }

  created_line_items = line_item_service.createLineItems([line_item_to_create])

  for line_item in created_line_items:
    return line_item