from datetime import datetime, timedelta
import os

# set these variables according to your experiments #
dir_path = 'data'
experiments_names = ['_baseline',
                     '_lava'
                     ]
runs = 3#10
limit_of_minutes = 10
# set these variables according to your experiments #

some_has_been_updated = False

while 1:

    # 10 minutes (do update this according to limit_of_minutes!
    os.system(" sleep 600s")

    youngest = []
    for exp in experiments_names:
        for run in range(0, runs):

            path = dir_path + "/" + exp +'_'+str(run+1) + "/data_fullevolution/fitness"
            if os.path.isdir(path):
                files = []
                for r, d, f in os.walk(path):
                    for file in f:
                        filetime = datetime.fromtimestamp(os.path.getctime(path+'/'+file))
                        files.append(filetime)
                files.sort()
                youngest.append(files[-1])
                time_now = datetime.now()
                time_ago = time_now - timedelta(minutes=limit_of_minutes)

                if files[-1] > time_ago:
                     some_has_been_updated = True

    if not some_has_been_updated:
       youngest.sort()
       print(str(time_now) + ': youngest file from ' + str(youngest[-1]))
       os.system(" kill $(  ps aux | grep 'gzserver' | awk '{print $2}')")
       os.system(" kill $(  ps aux | grep 'revolve.py' | awk '{print $2}')")
       print('  killled gzserver and revolve.py to force an error!')

    some_has_been_updated = False

