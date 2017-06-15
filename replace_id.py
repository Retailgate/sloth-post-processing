import json
import sys
import time

#print(sys.argv)
if len(sys.argv) < 4:
  print('Usage:   python replace_id.py INPUT_JSON_FILE -sSTART_FRAME -eEND_FRAME')
  print('Example:    python replace_id.py ch5.json -s2703 -e3603')
  exit()

for arg in sys.argv:
  if arg.startswith('-s'):
    start = int(arg[2:])
  elif arg.startswith('-e'):
    stop = int(arg[2:])
  else:
    input_file_name = arg
    output_file_name = 'replaced_' + input_file_name

person = {}

find = input('Enter ID to find: ')
replace = input('Replace ID %d with: ' % find)
exec_start = time.time()

with open(input_file_name, 'r') as data_file:
  data = json.load(data_file)
  output_data = []
  changes = 0
  for aClass in data:
    print(aClass['class'] + ', ' + aClass['filename'])
    interest = range(start, stop+1)
    for i, aFrame in enumerate(aClass['frames']):
      if aFrame['num'] in interest:
        for j, aNote in enumerate(aFrame['annotations']):
          if aNote['id'] == find:
            aClass['frames'][i]['annotations'][j]['id'] = replace
            changes += 1
    output_data.append(aClass)
  print('replaced in %d locations' % changes)
    
  with open(output_file_name, 'w') as output_file:
    print('writing output file')
    json.dump(output_data, output_file, sort_keys=True, indent=4)
print('done in %ss' % (time.time() - exec_start))
