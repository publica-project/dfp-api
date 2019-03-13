import googleads
import client

ga_client = client.get_client()
user_service = ga_client.GetService('UserService', version='v201811')

def get(email):
  if email is None:
    return None
    
  statement = (googleads.ad_manager.StatementBuilder()
               .Where('email = :email')
               .WithBindVariable('email', email))

  response = user_service.getUsersByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for user in response['results']:
      return user
  
  return None

def printOut():
  statement = googleads.ad_manager.StatementBuilder()
  
  response = user_service.getUsersByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    print('Found %s User(s):' % len(response['results']))
    for user in response['results']:
      print('  "%s" with ID "%s" and email "%s".' % (user['name'], user['id'], user['email']))
  
  else:
    print('No Users found.')

  print('')

if __name__ == '__main__':
  printOut()