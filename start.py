import os
print('starting codeserver.')
os.system('cd ./ && docker-compose up -d')
print('starting database..')
os.system('cd ./data && docker-compose up -d')
print('starting workers...')
os.system('cd ./workers/scripts && docker-compose up -d')
print('all done!')