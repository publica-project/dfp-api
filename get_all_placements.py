# Import appropriate modules from the client library.
from googleads import ad_manager

from client import get_client

def main(client):
  # Initialize appropriate service.
  placement_service = client.GetService('PlacementService', version='v201811')

  # Create a statement to select placements.
  statement = ad_manager.StatementBuilder(version='v201811')

  # Retrieve a small amount of placements at a time, paging
  # through until all placements have been retrieved.
  while True:
    response = placement_service.getPlacementsByStatement(statement.ToStatement(
    ))
    if 'results' in response and len(response['results']):
      for placement in response['results']:
        # Print out some information for each placement.
        print('ID: "%d"\nname: "%s"\n' %
              (placement['id'], placement['name']))
      statement.offset += statement.limit
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']


if __name__ == '__main__':
  ad_manager_client = get_client()
  main(ad_manager_client)