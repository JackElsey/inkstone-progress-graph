import glob
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime

mature_threshold = 7

num_backups = len(glob.glob('*.bak'))

young_counts = [0] * num_backups
mature_counts = [0] * num_backups

filenames = glob.glob('*.bak')
k = -1
for filename in filenames:
    k += 1

    with open(filename) as file_object:
        x = json.load(file_object)

    durations = []
    for i in range(0,16):
        vocab_status_entry = x['database']['table.vocabulary.{}'.format(i)]
        entry_split = re.split(r",",vocab_status_entry)
        for j in range(1,len(entry_split),7):
            try:
            	durations.append(int(entry_split[j+1])-int(entry_split[j]))
            except:
            	pass

    for duration in durations:
        if duration/60/60/24 < mature_threshold:
            young_counts[k] += 1
        else:
            mature_counts[k] += 1

backup_dates = []
for filename in filenames:
    backup_dates.append(datetime.strptime(filename[9:19],'%Y-%m-%d'))

backup_dates_sorted = sorted(backup_dates)
mature_counts_sorted = [y for _, y in sorted(zip(backup_dates,mature_counts), key=lambda pair: pair[0])]
young_counts_sorted = [y for _, y in sorted(zip(backup_dates,young_counts), key=lambda pair: pair[0])]

plt.style.use('seaborn-whitegrid')
fig,ax = plt.subplots()
ax.stackplot(backup_dates_sorted, mature_counts_sorted, young_counts_sorted,colors=[(0, .8, 0, 0.8),(0, 1, 0, 0.5)])
ax.set_title('Inkstone Study Progress')
ax.set_xlabel('date')
ax.set_ylabel('words')
ax.legend(['mature','young'],loc='upper left')
# ax.set_xlim(backup_dates_sorted[0],datetime(YYYY,M,D))
# ax.set_ylim(0,5000)
plt.show()
