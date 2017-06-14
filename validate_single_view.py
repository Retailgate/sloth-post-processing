import json
import sys
import time

exec_start = time.time()

#print(sys.argv)
if len(sys.argv) < 4:
  print('Usage:   python validate_singe_view.py INPUT_JSON_FILE -sSTART_FRAME -eEND_FRAME')
  print('Example:    python validate_singe_view.py ch5.json -s2703 -e3603')
  exit()

for arg in sys.argv:
  if arg.startswith('-s'):
    start = int(arg[2:])
  elif arg.startswith('-e'):
    stop = int(arg[2:])
  else:
    input_file_name = arg
    output_file_name = 'val_' + input_file_name

reps = []
missing = []
reps_count = 0
missing_count = 0

checks = ['area', 'gender', 'id']

with open(input_file_name, 'r') as data_file:
  data = json.load(data_file)
  for aClass in data:
    print(aClass['class'] + ', ' + aClass['filename'])
    frames = aClass['frames']
    relevant = filter(lambda x: (x['num'] <= stop) and (x['num'] >= start), frames)
    print('got ' + str(len(relevant)) + ' frames')
    for aFrame in relevant:
      notes = aFrame['annotations']
      ids = []
      for aNote in notes:
        if aNote['id'] in ids:
          print('repeated %d in frame %d' % (aNote['id'], aFrame['num']) )
          reps.append({str(aFrame['num']): aNote['id']})
          reps_count += 1
        ids.append(aNote['id'])
        for check in checks:
          if (not check in aNote) or (aNote[check] == None):
            print('empty %s for %d in frame %d' % (check, aNote['id'], aFrame['num']))
            missing.append({str(aFrame['num']): aNote['id']})
            missing_count += 1
  print('total repeated: %d' % reps_count)
  print('total missing: %d' % missing_count)
  with open(output_file_name, 'w') as output_file:
    print('writing output file')
    json.dump({'reps': reps, 'missing': missing}, output_file, sort_keys=True, indent=4)
print('done in %ss' % (time.time() - exec_start))
