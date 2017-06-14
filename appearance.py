import json
import sys
import time

exec_start = time.time()

#print(sys.argv)
if len(sys.argv) < 4:
  print('Usage:   python appearance.py INPUT_JSON_FILE -sSTART_FRAME -eEND_FRAME')
  print('Example:    python appearance.py ch5.json -s2703 -e3603')
  exit()

for arg in sys.argv:
  if arg.startswith('-s'):
    start = int(arg[2:])
  elif arg.startswith('-e'):
    stop = int(arg[2:])
  else:
    input_file_name = arg
    output_file_name = 'app_' + input_file_name

person = {}

with open(input_file_name, 'r') as data_file:
  data = json.load(data_file)
  for aClass in data:
    print(aClass['class'] + ', ' + aClass['filename'])
    frames = aClass['frames']
    relevant = filter(lambda x: (x['num'] <= stop) and (x['num'] >= start), frames)
    print('got ' + str(len(relevant)) + ' frames')
    for aFrame in relevant:
      notes = aFrame['annotations']
      for aNote in notes:
        if not aNote['id'] in person:
          print('adding ' + str(aNote['id']))
          person[aNote['id']] = [{'start': aFrame['num'], 'end': aFrame['num']}]
        else:
          moved = False;
          for presence in person[aNote['id']]:
            if presence['end'] - aFrame['num'] == -1:
              presence['end'] = aFrame['num']
              moved = True
          if not moved:
            print('adding new appearance for ' + str(aNote['id']))
            person[aNote['id']].append({'start': aFrame['num'], 'end': aFrame['num']})
  with open(output_file_name, 'w') as output_file:
    print('writing output file')
    json.dump(person, output_file, sort_keys=True, indent=4)
print('done in %ss' % (time.time() - exec_start))
