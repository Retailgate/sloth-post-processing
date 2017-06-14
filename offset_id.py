import json
import sys
import time

#print(sys.argv)
if len(sys.argv) < 4:
  print('Usage:   python offset_id.py INPUT_JSON_FILE -sSTART_FRAME -eEND_FRAME')
  print('Example:    python offset_id.py ch5.json -s2703 -e3603')
  exit()

for arg in sys.argv:
  if arg.startswith('-s'):
    start = int(arg[2:])
  elif arg.startswith('-e'):
    stop = int(arg[2:])
  else:
    input_file_name = arg
    output_file_name = 'offset_' + input_file_name

person = {}

with open(input_file_name, 'r') as data_file:
  data = json.load(data_file)
  output_data = []
  for aClass in data:
    print(aClass['class'] + ', ' + aClass['filename'])
    frames = aClass['frames']
    relevant = filter(lambda x: (x['num'] <= stop) and (x['num'] >= start), frames)
    print('got ' + str(len(relevant)) + ' frames')
    ids = []
    for aFrame in relevant:
      notes = aFrame['annotations']
      for aNote in notes:
        if not aNote['id'] in ids:
          #print('adding ' + str(aNote['id']))
          ids.append(aNote['id'])
    ids.sort()
    print('got the following IDs:', ids)
    offset = int(input('Enter the offset to add: '))
    print('\nPreview:');
    for anId in ids:
      print('%d  ->\t%d' % (anId, anId + offset))
    proceed = raw_input('Proceed? (y/n) ')
    if proceed != 'y':
      exit()
    exec_start = time.time()
    #TODO implement lookup table in first iteration for index to avoid searching
    for i in range(start, stop+1):
      match = None
      for index, item in enumerate(aClass['frames']):
        if item['num'] == i:
          match = index
          break
      if match:
        for index, item in enumerate(aClass['frames'][match]['annotations']):
          aClass['frames'][match]['annotations'][index]['id'] += offset
    output_data.append(aClass)
    
  with open(output_file_name, 'w') as output_file:
    print('writing output file')
    json.dump(output_data, output_file, sort_keys=True, indent=4)
print('done in %ss' % (time.time() - exec_start))
